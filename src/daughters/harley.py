"""
Harley Daughter Agent
Handles small tasks, messaging, opening apps
"""

import sys
import os
import subprocess
import platform

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Harley:
    def __init__(self):
        self.name = "Harley"
        self.kids = {
            "Groot": None,   # Executer
            "Rover": None,   # Thinker
            "Parker": None   # Charismatic
        }
    
    def handle_task(self, intent, params):
        """Route task to appropriate kid"""
        
        if intent == "open_app":
            app = params.get("app", "")
            return self._open_application(app)
        
        elif intent == "send_message":
            recipient = params.get("recipient", "unknown")
            content = params.get("content", "")
            return self._simulate_message(recipient, content)
        
        else:
            return {"status": "error", "message": f"Harley can't handle {intent}"}
    
    def _open_application(self, app_name):
        """Open an application based on OS"""
        system = platform.system()
        
        # Common app mappings
        app_commands = {
            "firefox": "firefox",
            "chrome": "google-chrome",
            "browser": "firefox",
            "terminal": "gnome-terminal",
            "code": "code",
            "vscode": "code",
            "calculator": "gnome-calculator",
            "files": "nautilus"
        }
        
        command = app_commands.get(app_name.lower(), app_name)
        
        try:
            if system == "Linux":
                subprocess.Popen([command])
            elif system == "Windows":
                os.startfile(command)
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", command])
            else:
                return {"status": "error", "message": f"Unsupported OS for opening apps"}
            
            return {"status": "success", "message": f"Opening {app_name}"}
        
        except FileNotFoundError:
            return {"status": "error", "message": f"Couldn't find '{app_name}'. Is it installed?"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to open: {str(e)}"}
    
    def _simulate_message(self, recipient, content):
        """Simulate sending a message (will integrate with real APIs later)"""
        # For now, just log it
        print(f"\n📱 [MESSAGE SIMULATION] To: {recipient} | Content: {content}")
        
        return {
            "status": "success",
            "message": f"I'll let {recipient} know: '{content}'"
        }

if __name__ == "__main__":
    harley = Harley()
    result = harley.handle_task("open_app", {"app": "firefox"})
    print(result)
