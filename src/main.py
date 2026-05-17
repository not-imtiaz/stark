"""
S.T.A.R.K. Main Entry Point
Connects: Your Voice/Text → Groq Translator → Father STARK → Output
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from translator.groq_translator import GroqTranslator
from father.stark_core import FatherSTARK

class STARKSystem:
    def __init__(self):
        print("Loading translator...")
        self.translator = GroqTranslator()
        print("Loading Father STARK...")
        self.father = FatherSTARK()
        print("\n" + "="*60)
        print("🟢 S.T.A.R.K. System Online")
        print("   Simple Tool AI Running Keytasks")
        print("   Translator: Groq (Free LLM)")
        print("="*60 + "\n")
    
    def process(self, user_input):
        """Process a single command from user"""
        if user_input.lower() in ["exit", "quit", "bye", "shutdown"]:
            print("\n🟢 STARK: Shutting down. I'll remember everything.")
            return False
        
        # Step 1: Translate human speech to JSON
        command = self.translator.translate(user_input)
        
        # Step 2: Send to Father STARK
        result = self.father.process_command(command)
        
        # Step 3: Get one-line response
        response = self.father.report_one_line(result)
        
        # Step 4: Display to user
        print(f"\n👤 You: {user_input}")
        print(f"🟢 STARK: {response}")
        
        # If error, show more details
        if result["status"] == "error":
            print(f"  └─ Details: {result.get('message', 'Unknown error')}")
            if "error_log" in result:
                print(f"  └─ Log: {result['error_log']}")
        
        return True
    
    def run_cli(self):
        """Run command-line interface (text only)"""
        print("💬 Type your commands (or 'exit' to quit):\n")
        print("Examples:")
        print("  • Set wallpaper.png as my background")
        print("  • Research quantum computing")
        print("  • Tell Sarah I'll be late")
        print("  • Defend my system")
        print("  • Open Firefox\n")
        
        while True:
            try:
                user_input = input("> ").strip()
                if user_input:
                    if not self.process(user_input):
                        break
            except KeyboardInterrupt:
                print("\n\n🟢 STARK: Shutting down.")
                break
            except Exception as e:
                print(f"🔴 STARK: An error occurred: {e}")

if __name__ == "__main__":
    stark_system = STARKSystem()
    
    # Ask if user wants to run tests
    print("Run quick tests? (y/n): ", end="")
    try:
        run_tests = input().lower() == 'y'
    except:
        run_tests = False
    
    if run_tests:
        print("\n--- Running Test Commands ---\n")
        test_commands = [
            "set wallpaper.png as my background",
            "research quantum computing", 
            "tell Tony I'm late",
            "defend my system",
            "open Firefox"
        ]
        
        for cmd in test_commands:
            stark_system.process(cmd)
            print()
        
        print("\n" + "="*60)
    
    print("\n🎯 Entering interactive mode...")
    print("="*60 + "\n")
    stark_system.run_cli()
