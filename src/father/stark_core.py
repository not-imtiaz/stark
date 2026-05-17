"""
S.T.A.R.K. Father Agent — Core (Updated with open_app)
"""

import json
import os
from datetime import datetime

class FatherSTARK:
    def __init__(self):
        self.name = "STARK"
        self.capability_registry = self._load_registry()
        self.task_history = []
        self.memory_path = "stark_data/memory/father_memory.json"
        self._ensure_directories()
    
    def _ensure_directories(self):
        os.makedirs("stark_data/memory", exist_ok=True)
        os.makedirs("stark_data/logs", exist_ok=True)
    
    def _load_registry(self):
        """Define what each daughter can do"""
        return {
            "Morgan": {
                "domain": ["code", "app", "hardware", "software", "wallpaper", "file", "build", "create"],
                "success_rate": 1.0,
                "avg_time_ms": 800
            },
            "Peter": {
                "domain": ["research", "study", "summary", "search", "learn", "read", "find"],
                "success_rate": 0.88,
                "avg_time_ms": 1200
            },
            "Harley": {
                "domain": ["message", "alarm", "remind", "open", "close", "small", "send", "notify", "launch"],
                "success_rate": 0.91,
                "avg_time_ms": 500
            },
            "Ultron": {
                "domain": ["defend", "lockdown", "threat", "block", "secure", "heavy", "protect", "guard"],
                "success_rate": 0.85,
                "avg_time_ms": 2100
            }
        }
    
    def _match_domain(self, intent, params):
        """Match task to best daughter — returns None if no match"""
        task_text = f"{intent} {json.dumps(params)}".lower()
        
        best_daughter = None
        best_score = 0
        
        for daughter, data in self.capability_registry.items():
            # Count keyword matches
            matches = sum(1 for keyword in data["domain"] if keyword in task_text)
            
            # Only consider if at least one keyword matched
            if matches > 0:
                score = matches + data["success_rate"]
                if score > best_score:
                    best_score = score
                    best_daughter = daughter
        
        return best_daughter
    
    def process_command(self, json_command):
        """Main entry point — receives JSON from DeepSeek"""
        intent = json_command.get("intent")
        params = json_command.get("params", {})
        
        # Special handling for intents that need explicit mapping
        intent_to_domain = {
            "open_app": "open",  # maps to Harley's "open" keyword
            "set_wallpaper": "wallpaper",
            "send_message": "message",
            "research": "research",
            "defend": "defend",
            "code": "code"
        }
        
        # Add the intent as a keyword if needed
        if intent in intent_to_domain:
            keyword = intent_to_domain[intent]
            # Temporarily add to params for matching
            temp_params = params.copy()
            temp_params["_keyword"] = keyword
        else:
            temp_params = params
        
        # Match to daughter
        daughter = self._match_domain(intent, temp_params)
        
        if daughter is None:
            error_file = self._save_error(intent, params)
            return {
                "status": "error",
                "message": f"I don't know how to handle '{intent}'. Try: set_wallpaper, research, send_message, open_app, code, defend",
                "error_log": error_file
            }
        
        # Log task
        task_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.task_history.append({
            "task_id": task_id,
            "intent": intent,
            "assigned_to": daughter,
            "params": params
        })
        
        self._save_memory()
        
        return {
            "status": "assigned",
            "task_id": task_id,
            "assigned_to": daughter,
            "message": f"Assigned '{intent}' to {daughter}"
        }
    
    def _save_error(self, intent, params):
        """Save unknown command to error log"""
        import glob
        existing = glob.glob("stark_data/logs/error_*.txt")
        next_num = len(existing) + 1
        error_file = f"stark_data/logs/error_{next_num:03d}.txt"
        
        with open(error_file, 'w') as f:
            f.write(f"TIMESTAMP: {datetime.now()}\n")
            f.write(f"ERROR: Unknown intent '{intent}'\n")
            f.write(f"PARAMS: {json.dumps(params)}\n")
            f.write(f"SUGGESTION: Use one of: set_wallpaper, research, send_message, open_app, code, defend\n")
        
        return error_file
    
    def _save_memory(self):
        memory = {
            "task_history": self.task_history[-100:],
            "capability_registry": self.capability_registry
        }
        with open(self.memory_path, 'w') as f:
            json.dump(memory, f, indent=2)
    
    def report_one_line(self, result):
        if result["status"] == "assigned":
            return f"{result['assigned_to']} is handling your request."
        elif result["status"] == "error":
            return f"Error: {result['message']}"
        return result.get("message", "Task completed.")
    
    def show_status(self):
        print("\n" + "="*50)
        print(f"S.T.A.R.K. System Status")
        print("="*50)
        print(f"Father Agent: {self.name} (active)")
        print(f"Tasks handled: {len(self.task_history)}")
        print("\nDaughter Agents:")
        for daughter, data in self.capability_registry.items():
            print(f"  - {daughter}: {data['success_rate']*100:.0f}% success, {data['avg_time_ms']}ms avg")
        print("="*50)

if __name__ == "__main__":
    stark = FatherSTARK()
    print("Father STARK ready. Run 'python3 src/main.py' to start full system.")
