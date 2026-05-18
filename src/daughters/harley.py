"""
Harley Daughter Agent - Simple working version
"""

import subprocess
import shutil
from datetime import datetime

class Harley:
    def __init__(self):
        self.name = "Harley"
    
    def handle_task(self, intent, params):
        if intent == "open_app":
            app = params.get("app", "")
            if not app:
                return {"status": "error", "message": "Which app would you like to open?"}
            return self._open_application(app)
        
        elif intent == "send_message":
            recipient = params.get("recipient", "someone")
            content = params.get("content", "")
            print(f"\n📱 [MESSAGE] To: {recipient} | {content}")
            return {"status": "success", "message": f"I'll tell {recipient}: '{content}'"}
        
        elif intent == "get_time":
            now = datetime.now()
            time_str = now.strftime("%I:%M %p").lstrip("0")
            return {"status": "success", "message": f"🕐 It's {time_str}"}
        
        else:
            return {"status": "error", "message": f"Harley can't handle {intent}"}
    
    def _open_application(self, app_name):
        """Open an application"""
        app_lower = app_name.lower()
        
        # Common app mappings
        app_map = {
            "firefox": "firefox",
            "chrome": "google-chrome",
            "chromium": "chromium-browser",
            "terminal": "gnome-terminal",
            "code": "code",
            "calculator": "gnome-calculator",
            "files": "nautilus",
            "settings": "gnome-control-center"
        }
        
        # Get the actual command
        cmd = app_map.get(app_lower, app_lower)
        
        # Find the executable
        exe_path = shutil.which(cmd)
        
        if exe_path:
            try:
                subprocess.Popen([exe_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return {"status": "success", "message": f"Opening {app_name}"}
            except Exception as e:
                return {"status": "error", "message": f"Failed to open: {str(e)}"}
        else:
            return {"status": "error", "message": f"Couldn't find '{app_name}'. Try 'firefox', 'terminal', or 'calculator'."}

# Test when run directly
if __name__ == "__main__":
    h = Harley()
    
    # Test open app
    result = h.handle_task("open_app", {"app": "firefox"})
    print("Open Firefox:", result)
    
    # Test get time
    result = h.handle_task("get_time", {})
    print("Get time:", result)
    
    # Test send message
    result = h.handle_task("send_message", {"recipient": "Tony", "content": "Hello"})
    print("Send message:", result)

    def _send_whatsapp(self, recipient, message):
        """Send real WhatsApp message (opens web.whatsapp.com)"""
        try:
            import pywhatkit as kit
            import datetime
            
            # Get current time + 1 minute (pywhatkit needs future time)
            now = datetime.datetime.now()
            send_time = now + datetime.timedelta(minutes=1)
            
            # Note: This will open WhatsApp Web in browser
            kit.sendwhatmsg(recipient, message, send_time.hour, send_time.minute)
            
            return {"status": "success", "message": f"WhatsApp message scheduled for {recipient} at {send_time.strftime('%H:%M')}"}
        except Exception as e:
            return {"status": "error", "message": f"WhatsApp failed: {str(e)}"}

    def _send_whatsapp(self, recipient, message):
        """Send real WhatsApp message (opens web.whatsapp.com)"""
        try:
            import pywhatkit as kit
            import datetime
            
            # Get current time + 1 minute (pywhatkit needs future time)
            now = datetime.datetime.now()
            send_time = now + datetime.timedelta(minutes=1)
            
            # Note: This will open WhatsApp Web in browser
            kit.sendwhatmsg(recipient, message, send_time.hour, send_time.minute)
            
            return {"status": "success", "message": f"WhatsApp message scheduled for {recipient} at {send_time.strftime('%H:%M')}"}
        except Exception as e:
            return {"status": "error", "message": f"WhatsApp failed: {str(e)}"}
    def get_kids(self):
        return ["Groot", "Rover", "Parker"]
