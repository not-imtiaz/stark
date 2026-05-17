"""
JARVIS - Frontend/UI Kid
Handles wallpaper setting, UI changes, visual tasks
"""

import os
import subprocess
import platform

class JARVIS:
    def __init__(self):
        self.name = "JARVIS"
        self.parent = "Morgan"
    
    def set_wallpaper(self, filepath):
        """Set desktop wallpaper from image file"""
        
        # Check if file exists
        if not os.path.exists(filepath):
            # Search common locations
            search_paths = [
                filepath,
                os.path.expanduser(f"~/Desktop/{filepath}"),
                os.path.expanduser(f"~/Pictures/{filepath}"),
                os.path.expanduser(f"~/Downloads/{filepath}"),
                os.path.expanduser(f"~/{filepath}")
            ]
            
            found = None
            for path in search_paths:
                if os.path.exists(path):
                    found = path
                    break
            
            if not found:
                return {"status": "error", "message": f"File not found: {filepath}"}
            filepath = found
        
        # Set wallpaper based on OS
        system = platform.system()
        
        try:
            if system == "Linux":
                # Try GNOME first
                if os.path.exists("/usr/bin/gsettings"):
                    subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{filepath}"])
                    return {"status": "success", "message": f"Wallpaper set to {filepath} (GNOME)"}
                elif os.path.exists("/usr/bin/xfconf-query"):
                    subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", "/backdrop/screen0/monitor0/image-path", "-s", filepath])
                    return {"status": "success", "message": f"Wallpaper set to {filepath} (XFCE)"}
                else:
                    return {"status": "error", "message": "Unsupported Linux desktop. Try GNOME or XFCE."}
            
            elif system == "Windows":
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 3)
                return {"status": "success", "message": f"Wallpaper set to {filepath}"}
            
            elif system == "Darwin":  # macOS
                subprocess.run(["osascript", "-e", f'tell application "Finder" to set desktop picture to POSIX file "{filepath}"'])
                return {"status": "success", "message": f"Wallpaper set to {filepath}"}
            
            else:
                return {"status": "error", "message": f"Unsupported OS: {system}"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def execute(self, task, params):
        """Main execution method"""
        if task == "set_wallpaper":
            file = params.get("file", "wallpaper.png")
            return self.set_wallpaper(file)
        else:
            return {"status": "error", "message": f"Unknown task: {task}"}

# Test
if __name__ == "__main__":
    jarvis = JARVIS()
    result = jarvis.execute("set_wallpaper", {"file": "wallpaper.png"})
    print(result)
