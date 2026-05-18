"""
Bridge between STARK Father Agent and Dashboard
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from father.stark_core import FatherSTARK
from translator.groq_translator import GroqTranslator

class StarkDashboardBridge:
    def __init__(self):
        self.stark = FatherSTARK()
        self.translator = GroqTranslator()
        self.task_history = []
    
    def process_command(self, command_text):
        """Process a command and return task data for dashboard"""
        
        # Translate human text to JSON
        command = self.translator.translate(command_text)
        
        # Process through Father STARK
        result = self.stark.process_command(command)
        
        # Format as dashboard task
        task = {
            "task_id": result.get("task_id", f"task_{int(time.time())}"),
            "type": command.get("type", "action"),
            "intent": command.get("intent", "unknown"),
            "params": command.get("params", {}),
            "summary": result.get("message", "")[:200],
            "full_text": result.get("message", ""),
            "query": command_text,
            "assigned_to": result.get("assigned_to", "STARK"),
            "timestamp": datetime.now().isoformat(),
            "status": result.get("status", "success"),
            "duration_ms": 0,
        }
        
        return task

if __name__ == "__main__":
    bridge = StarkDashboardBridge()
    result = bridge.process_command("what is a quantum computer")
    print(result)
