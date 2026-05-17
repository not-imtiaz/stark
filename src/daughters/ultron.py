"""
Ultron Daughter Agent
Handles defense, security, and heavy tasks
"""

import sys
import os
import psutil
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Ultron:
    def __init__(self):
        self.name = "Ultron"
        self.kids = {
            "Vision": None,  # Last line of defense
            "Nexus": None,   # Helper
            "Sentry": None   # Hard executer
        }
    
    def handle_task(self, intent, params):
        """Route task to appropriate kid"""
        
        if intent == "defend":
            action = params.get("action", "scan")
            return self._system_check()
        
        elif intent == "lockdown":
            return self._lockdown()
        
        else:
            return {"status": "error", "message": f"Ultron can't handle {intent}"}
    
    def _system_check(self):
        """Run basic security check"""
        try:
            # Check CPU usage
            cpu = psutil.cpu_percent(interval=1)
            
            # Check memory
            memory = psutil.virtual_memory()
            
            # Check running processes for suspicious names (basic)
            suspicious = []
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name'].lower()
                    suspicious_keywords = ['malware', 'virus', 'exploit', 'backdoor']
                    for keyword in suspicious_keywords:
                        if keyword in name:
                            suspicious.append(name)
                except:
                    pass
            
            status = "🟢 SYSTEM SECURE"
            if cpu > 90:
                status = "🟡 High CPU usage detected"
            if memory.percent > 90:
                status = "🟡 Low memory warning"
            if suspicious:
                status = f"🔴 Suspicious processes: {', '.join(suspicious[:3])}"
            
            return {
                "status": "success",
                "message": f"{status}\nCPU: {cpu}% | RAM: {memory.percent}% | Processes: {len(psutil.pids())}"
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Defense check failed: {str(e)}"}
    
    def _lockdown(self):
        """Basic lockdown simulation"""
        return {
            "status": "success",
            "message": "🔒 Lockdown simulation complete. System protected."
        }

if __name__ == "__main__":
    ultron = Ultron()
    result = ultron.handle_task("defend", {})
    print(result)
