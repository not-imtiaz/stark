"""
S.T.A.R.K. Father Agent — Complete with all daughters
"""

import json
import os
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
        self.task_history = []
        self.memory_path = "stark_data/memory/father_memory.json"
        self._ensure_directories()
    
    def _ensure_directories(self):
        os.makedirs("stark_data/memory", exist_ok=True)
        os.makedirs("stark_data/logs", exist_ok=True)
    
    def _match_daughter(self, intent, params):
        """Route intent to correct daughter"""
        
        # Intent to daughter mapping
        routing = {
            "set_wallpaper": "Morgan",
            "code": "Morgan",
            "delete_file": "Morgan",
            "research": "Peter",
            "open_app": "Harley",
            "send_message": "Harley",
            "get_time": "Harley",
            "defend": "Ultron",
            "lockdown": "Ultron"
        }
        
        # Check if intent is in routing table
        if intent in routing:
            return routing[intent]
        
        # Fallback to keyword matching
        task_text = f"{intent} {json.dumps(params)}".lower()
        
        if any(word in task_text for word in ["wallpaper", "file", "code", "app"]):
            return "Morgan"
        elif any(word in task_text for word in ["research", "search", "study"]):
            return "Peter"
        elif any(word in task_text for word in ["open", "launch", "message", "tell", "time"]):
            return "Harley"
        elif any(word in task_text for word in ["defend", "secure", "protect", "lockdown"]):
            return "Ultron"
        
        return None
    
    def process_command(self, json_command):
        intent = json_command.get("intent")
        params = json_command.get("params", {})
        
        daughter_name = self._match_daughter(intent, params)
        
        if daughter_name is None:
            error_file = self._save_error(intent, params)
            return {
                "status": "error",
                "message": f"I don't know how to handle '{intent}'",
                "error_log": error_file
            }
        
        daughter = self.daughters.get(daughter_name)
        
        if daughter is None:
            return {
                "status": "error",
                "message": f"Daughter {daughter_name} not implemented"
            }
        
        result = daughter.handle_task(intent, params)
        
        task_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.task_history.append({
            "task_id": task_id,
            "intent": intent,
            "assigned_to": daughter_name,
            "result": result
        })
        
        self._save_memory()
        
        return {
            "status": result.get("status", "completed"),
            "task_id": task_id,
            "assigned_to": daughter_name,
            "message": result.get("message", "Task completed"),
            "details": result
        }
    
    def _save_error(self, intent, params):
        import glob
        existing = glob.glob("stark_data/logs/error_*.txt")
        next_num = len(existing) + 1
        error_file = f"stark_data/logs/error_{next_num:03d}.txt"
        
        with open(error_file, 'w') as f:
            f.write(f"TIMESTAMP: {datetime.now()}\n")
            f.write(f"ERROR: Unknown intent '{intent}'\n")
            f.write(f"PARAMS: {json.dumps(params)}\n")
        
        return error_file
    
    def _save_memory(self):
        memory = {"task_history": self.task_history[-100:]}
        with open(self.memory_path, 'w') as f:
            json.dump(memory, f, indent=2)
    
    def report_one_line(self, result):
        if result["status"] == "error":
            return f"Error: {result['message']}"
        return result.get("message", f"{result['assigned_to']} completed the task")

if __name__ == "__main__":
    stark = FatherSTARK()
    print("Father STARK ready with all daughters!")
