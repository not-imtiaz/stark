"""
STARK AI Agent Dashboard - Flask + SocketIO Backend
Real-time monitoring interface for the STARK multi-agent system
"""

import json
import random
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import psutil
import os

app = Flask(__name__, static_folder=".")
app.config["SECRET_KEY"] = "stark-jarvis-secret-2024"
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ─────────────────────────────────────────────
# In-memory state (replace with DB in production)
# ─────────────────────────────────────────────

DAUGHTERS = {
    "Morgan": {
        "name": "Morgan",
        "role": "Coding & Engineering",
        "status": "idle",
        "current_task": None,
        "success_rate": 97.3,
        "tasks_completed": 142,
        "kids": ["Pepper", "Rhodes", "Happy"],
        "color": "#00D4FF",
    },
    "Peter": {
        "name": "Peter",
        "role": "Research & Knowledge",
        "status": "active",
        "current_task": "Querying quantum computing papers",
        "success_rate": 94.8,
        "tasks_completed": 209,
        "kids": ["MJ", "Ned", "Flash"],
        "color": "#7B61FF",
    },
    "Harley": {
        "name": "Harley",
        "role": "Actions & Automation",
        "status": "busy",
        "current_task": "Executing file system scan",
        "success_rate": 91.2,
        "tasks_completed": 88,
        "kids": ["Cassie", "Scott", "Hope"],
        "color": "#FF6B35",
    },
    "Ultron": {
        "name": "Ultron",
        "role": "Defense & Security",
        "status": "idle",
        "current_task": None,
        "success_rate": 99.1,
        "tasks_completed": 317,
        "kids": ["Vision", "Wanda", "Pietro"],
        "color": "#FF3864",
    },
}

TASK_TYPES = ["knowledge", "action", "conversation"]
TASK_INTENTS = {
    "knowledge": ["research", "summarize", "explain", "define", "compare"],
    "action":    ["execute", "automate", "schedule", "deploy", "monitor"],
    "conversation": ["chat", "assist", "clarify", "brainstorm", "plan"],
}

SAMPLE_QUERIES = [
    "Explain the concept of neural plasticity",
    "Deploy the staging environment",
    "Schedule a system backup for midnight",
    "Research latest advances in quantum error correction",
    "Summarize the weekly code commits",
    "Monitor network traffic for anomalies",
    "Brainstorm approaches for the new API design",
    "Compare transformer vs mamba architectures",
    "Execute database cleanup routine",
    "Plan the next sprint milestones",
    "Define Retrieval Augmented Generation",
    "Clarify the deployment pipeline steps",
]

SAMPLE_RESPONSES = [
    "Neural plasticity refers to the brain's ability to reorganize itself by forming new neural connections throughout life. This remarkable property allows neurons to compensate for injury and disease and to adjust their activities in response to new situations or changes in their environment. Research has shown that experience-dependent plasticity occurs throughout life, though it is generally stronger during critical periods of development.",
    "Quantum error correction is a set of methods used to protect quantum information from errors due to decoherence and other quantum noise. Recent advances include the surface code achieving below-threshold error rates at Google, Microsoft's topological qubit progress, and IBM's advances in fault-tolerant logical qubits. The field is rapidly approaching practical quantum advantage for specific computational tasks.",
    "Transformer architecture uses self-attention mechanisms to process sequences in parallel, making it highly parallelizable but memory-intensive for long sequences. Mamba uses selective state space models (SSMs) that process sequences recurrently, achieving linear scaling with sequence length. In practice, Mamba excels at very long context tasks while transformers still dominate most language modeling benchmarks. Hybrid architectures combining both are an active research frontier.",
    "Retrieval Augmented Generation (RAG) is a technique that enhances large language model outputs by retrieving relevant documents from an external knowledge base before generating a response. The system first embeds the query, searches a vector database for semantically similar chunks, then provides these chunks as context to the LLM. This reduces hallucinations and enables the model to access up-to-date or domain-specific information not present in its training data.",
]

# Initialize task history
task_history = []
task_counter = 0
system_start_time = datetime.now()
error_count_24h = 0


def _generate_task_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S") + f"_{random.randint(100, 999)}"


def _create_sample_task():
    global task_counter, error_count_24h
    task_counter += 1
    task_type = random.choice(TASK_TYPES)
    intent = random.choice(TASK_INTENTS[task_type])
    daughter = random.choice(list(DAUGHTERS.keys()))
    status = random.choices(
        ["success", "success", "success", "error"], weights=[85, 5, 5, 5])[0]
    if status == "error":
        error_count_24h += 1

    query = random.choice(SAMPLE_QUERIES)
    full_text = random.choice(SAMPLE_RESPONSES)

    task = {
        "task_id": _generate_task_id(),
        "type": task_type,
        "intent": intent,
        "params": {"topic": query.lower().replace(" ", "_")[:30]},
        "summary": full_text[:200] + "...",
        "full_text": full_text,
        "query": query,
        "assigned_to": daughter,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "duration_ms": random.randint(120, 3400),
    }
    return task


def _seed_history():
    """Populate initial task history."""
    now = datetime.now()
    for i in range(50):
        task = _create_sample_task()
        # Spread over last 24h
        offset = timedelta(minutes=random.randint(0, 1440))
        task["timestamp"] = (now - offset).isoformat()
        task_history.append(task)
    task_history.sort(key=lambda t: t["timestamp"], reverse=True)


_seed_history()


# ─────────────────────────────────────────────
# REST API Endpoints
# ─────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/history")
def get_history():
    """Returns last 50 tasks."""
    limit = int(request.args.get("limit", 50))
    return jsonify(task_history[:limit])


@app.route("/api/status")
def get_status():
    """Returns agent status for all daughters."""
    uptime_seconds = int((datetime.now() - system_start_time).total_seconds())
    return jsonify({
        "stark": {"status": "online", "uptime": uptime_seconds},
        "daughters": DAUGHTERS,
        "tasks_today": sum(1 for t in task_history
                           if t["timestamp"] > (datetime.now() - timedelta(hours=24)).isoformat()),
        "error_count_24h": error_count_24h,
        "total_tasks": len(task_history),
    })


@app.route("/api/command", methods=["POST"])
def send_command():
    """Accept a command and emit it as a task."""
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Missing 'command' field"}), 400

    task = _create_sample_task()
    task["query"] = data["command"]
    task["intent"] = "command"
    task["type"] = "conversation"
    task["timestamp"] = datetime.now().isoformat()
    task_history.insert(0, task)

    socketio.emit("task_update", task)
    return jsonify({"status": "dispatched", "task_id": task["task_id"]}), 202


# ─────────────────────────────────────────────
# Background simulation threads
# ─────────────────────────────────────────────

def emit_task_updates():
    """Periodically emit new tasks to simulate live activity."""
    while True:
        time.sleep(random.uniform(4, 10))
        task = _create_sample_task()
        task_history.insert(0, task)
        if len(task_history) > 500:
            task_history.pop()

        # Update daughter status
        daughter = DAUGHTERS[task["assigned_to"]]
        daughter["tasks_completed"] += 1
        if task["status"] == "success":
            daughter["current_task"] = None
            daughter["status"] = random.choice(["idle", "active"])
        else:
            daughter["status"] = "busy"

        socketio.emit("task_update", task)


def emit_agent_heartbeats():
    """Periodically emit daughter agent status."""
    while True:
        time.sleep(5)
        for name, d in DAUGHTERS.items():
            # Randomly fluctuate status
            if random.random() < 0.15:
                d["status"] = random.choice(["idle", "active", "busy"])
            socketio.emit("agent_status", {
                "name": name,
                "status": d["status"],
                "success_rate": round(d["success_rate"] + random.uniform(-0.2, 0.2), 1),
                "tasks_completed": d["tasks_completed"],
                "current_task": d["current_task"],
            })


def emit_system_metrics():
    """Emit real CPU/RAM metrics every 2 seconds."""
    while True:
        time.sleep(2)
        try:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
        except Exception:
            cpu = random.uniform(15, 65)
            ram = random.uniform(40, 75)

        socketio.emit("system_metrics", {
            "cpu": round(cpu, 1),
            "ram": round(ram, 1),
            "timestamp": datetime.now().isoformat(),
        })


# ─────────────────────────────────────────────
# SocketIO Events
# ─────────────────────────────────────────────

@socketio.on("connect")
def on_connect():
    print(f"[STARK] Client connected: {request.sid}")
    # Send initial snapshot
    emit("task_update", {"batch": task_history[:30]})
    emit("agent_status", {"batch": list(DAUGHTERS.values())})


@socketio.on("disconnect")
def on_disconnect():
    print(f"[STARK] Client disconnected: {request.sid}")


# ─────────────────────────────────────────────
# Start background threads
# ─────────────────────────────────────────────

def start_background_threads():
    t1 = threading.Thread(target=emit_task_updates, daemon=True)
    t2 = threading.Thread(target=emit_agent_heartbeats, daemon=True)
    t3 = threading.Thread(target=emit_system_metrics, daemon=True)
    t1.start()
    t2.start()
    t3.start()


start_background_threads()

if __name__ == "__main__":
    print("⚡ STARK Dashboard initializing on http://0.0.0.0:5000")
    socketio.run(app, host="0.0.0.0", port=5000,
                 debug=False, allow_unsafe_werkzeug=True)
