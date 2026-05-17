"""
Morgan Daughter Agent
Handles coding, hardware, system tasks
"""

import sys
import os

# Add parent directory to path so we can import kids
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from kids.morgan_kids
from kids.morgan_kids.jarvis import JARVIS

class Morgan:
    def __init__(self):
        self.name = "Morgan"
        self.kids = {
            "JARVIS": JARVIS(),
            "FRIDAY": None,  # Will add later
            "Jocasta": None   # Will add later
        }
    
    def handle_task(self, intent, params):
        """Route task to appropriate kid"""
        
        if intent == "set_wallpaper":
            result = self.kids["JARVIS"].execute("set_wallpaper", params)
            return result
        
        # More tasks will be added
        else:
            return {"status": "error", "message": f"Morgan can't handle {intent}"}

if __name__ == "__main__":
    morgan = Morgan()
    result = morgan.handle_task("set_wallpaper", {"file": "wallpaper.png"})
    print(result)
