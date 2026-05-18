"""
S.T.A.R.K. Father Agent - With Real Performance Tracking
"""

import json
import os
import time
from datetime import datetime
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from daughters.morgan import Morgan
from daughters.peter import Peter
from daughters.harley import Harley
from daughters.ultron import Ultron

class FatherSTARK:
    def __init__(self):
        self.name = "STARK"
        self.daughters = {
            "Morgan": Morgan(),
            "Peter": Peter(),
            "Harley": Harley(),
            "Ultron": Ultron()
        }
        self.performance = self._load_performance()
        self.task_history = []
        self.memory_path = "stark_data/memory/father_memory.json"
        self._ensure_directories()
        
        self.identity = {
            "name": "STARK",
            "full_name": "Simple Tool AI Running Keytasks",
            "purpose": "To assist with PC automation, research, tasks, and defense"
        }
    
    def _ensure_directories(self):
        os.makedirs("stark_data/memory", exist_ok=True)
        os.makedirs("stark_data/logs", exist_ok=True)
    
    def _load_performance(self):
        """Load performance data from disk"""
        perf_path = "stark_data/memory/performance.json"
        if os.path.exists(perf_path):
            with open(perf_path, 'r') as f:
                return json.load(f)
        return {
            "Morgan": {"success": 0, "fail": 0, "total_time": 0, "tasks": 0},
            "Peter": {"success": 0, "fail": 0, "total_time": 0, "tasks": 0},
            "Harley": {"success": 0, "fail": 0, "total_time": 0, "tasks": 0},
            "Ultron": {"success": 0, "fail": 0, "total_time": 0, "tasks": 0}
        }
    
    def _save_performance(self):
        """Save performance data to disk"""
        perf_path = "stark_data/memory/performance.json"
        with open(perf_path, 'w') as f:
            json.dump(self.performance, f, indent=2)
    
    def _update_performance(self, agent_name, success, duration_ms):
        """Update real performance metrics"""
        perf = self.performance.get(agent_name)
        if perf:
            if success:
                perf["success"] += 1
            else:
                perf["fail"] += 1
            perf["total_time"] += duration_ms
            perf["tasks"] += 1
            self._save_performance()
    
    def get_success_rate(self, agent_name):
        """Calculate real success rate"""
        perf = self.performance.get(agent_name, {})
        total = perf.get("success", 0) + perf.get("fail", 0)
        if total == 0:
            return 100.0
        return round((perf["success"] / total) * 100, 1)
    
    def get_avg_time(self, agent_name):
        """Calculate real average response time"""
        perf = self.performance.get(agent_name, {})
        tasks = perf.get("tasks", 0)
        if tasks == 0:
            return 0
        return round(perf["total_time"] / tasks, 0)
    
    def get_agent_status(self):
        """Return real-time agent status with performance data"""
        status = {}
        for name in self.daughters.keys():
            status[name] = {
                "name": name,
                "status": "active" if self.daughters[name] else "idle",
                "success_rate": self.get_success_rate(name),
                "avg_response_ms": self.get_avg_time(name),
                "tasks_completed": self.performance[name]["success"],
                "tasks_failed": self.performance[name]["fail"],
                "kids": self.daughters[name].get_kids() if hasattr(self.daughters[name], 'get_kids') else []
            }
        return status
    
    def _handle_conversation(self, intent, params):
        if intent == "identity":
            msg = f"I am {self.identity['full_name']}. {self.identity['purpose']}"
            return {"status": "success", "message": msg, "full_text": msg, "summary": msg}
        elif intent == "capability":
            msg = "I can set wallpaper, open apps, research topics, send messages, defend your system, and more."
            return {"status": "success", "message": msg, "full_text": msg, "summary": msg}
        elif intent == "greeting":
            msg = "Hello boss. STARK is ready. How can I help?"
            return {"status": "success", "message": msg, "full_text": msg, "summary": msg}
        else:
            msg = "STARK is online and ready. What do you need?"
            return {"status": "success", "message": msg, "full_text": msg, "summary": msg}
    
    def _handle_action(self, intent, params):
        routing = {
            "set_wallpaper": "Morgan",
            "open_app": "Harley",
            "send_message": "Harley",
            "defend": "Ultron",
        }
        
        daughter_name = routing.get(intent)
        if not daughter_name:
            return {"status": "error", "message": f"Unknown action: {intent}"}
        
        daughter = self.daughters.get(daughter_name)
        if not daughter:
            return {"status": "error", "message": f"Daughter {daughter_name} not available"}
        
        start_time = time.time()
        result = daughter.handle_task(intent, params)
        duration_ms = int((time.time() - start_time) * 1000)
        
        success = result.get("status") == "success"
        self._update_performance(daughter_name, success, duration_ms)
        result["duration_ms"] = duration_ms
        
        return result
    
    def _handle_knowledge(self, intent, params):
        topic = params.get("topic", "")
        if not topic:
            return {"status": "error", "message": "What would you like me to research?"}
        
        start_time = time.time()
        result = self.daughters["Peter"].handle_task("research", {"topic": topic})
        duration_ms = int((time.time() - start_time) * 1000)
        
        success = result.get("status") == "success"
        self._update_performance("Peter", success, duration_ms)
        result["duration_ms"] = duration_ms
        
        return result
    
    def process_command(self, json_command):
        command_type = json_command.get("type", "action")
        intent = json_command.get("intent", "unknown")
        params = json_command.get("params", {})
        
        if command_type == "conversation":
            result = self._handle_conversation(intent, params)
            assigned_to = "STARK"
        elif command_type == "knowledge":
            result = self._handle_knowledge(intent, params)
            assigned_to = "Peter"
        else:
            result = self._handle_action(intent, params)
            assigned_to = result.get("assigned_to", "Unknown")
        
        task_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        task_entry = {
            "task_id": task_id,
            "type": command_type,
            "intent": intent,
            "params": params,
            "summary": result.get("summary", result.get("message", "")),
            "full_text": result.get("full_text", result.get("message", "")),
            "assigned_to": assigned_to,
            "status": result.get("status", "success"),
            "duration_ms": result.get("duration_ms", 0),
            "timestamp": datetime.now().isoformat()
        }
        self.task_history.append(task_entry)
        
        voice_message = result.get("summary", result.get("message", "Task completed"))
        
        return {
            "status": result.get("status", "completed"),
            "task_id": task_id,
            "assigned_to": assigned_to,
            "message": voice_message,
            "full_response": result,
            "task_entry": task_entry
        }
    
    def report_one_line(self, result):
        if result["status"] == "error":
            return f"Error: {result['message']}"
        return result.get("message", "Task completed")
    
    def get_task_history(self):
        return self.task_history[-50:]

if __name__ == "__main__":
    stark = FatherSTARK()
    print("Father STARK ready with real performance tracking!")
