"""
DeepSeek Translator — Converts human speech to JSON commands for Father STARK
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

class DeepSeekTranslator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.system_prompt = """
You are STARK's translator. Convert human commands into JSON machine language.
Output ONLY valid JSON. No explanation. No extra text.

Possible intents:
- set_wallpaper : change desktop background
- research : search for information
- send_message : send a message (WhatsApp, etc.)
- code : write or run code
- defend : security or protection tasks
- open_app : launch an application
- unknown : if you cannot understand

Example 1: "set wallpaper.png as my background"
Output: {"intent": "set_wallpaper", "params": {"file": "wallpaper.png"}}

Example 2: "research quantum computing"
Output: {"intent": "research", "params": {"topic": "quantum computing", "depth": "summary"}}

Example 3: "tell Tony I'm running late"
Output: {"intent": "send_message", "params": {"recipient": "Tony", "content": "I'm running late", "platform": "whatsapp"}}

Example 4: "open Firefox"
Output: {"intent": "open_app", "params": {"app": "firefox"}}

If you cannot understand the command:
Output: {"intent": "unknown", "params": {"original": "user's exact words"}}
"""
    
    def translate(self, user_input):
        """Convert human speech to JSON command"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1
            )
            
            # Parse the JSON response
            command = json.loads(response.choices[0].message.content)
            return command
            
        except Exception as e:
            # If API fails, return an error command
            return {
                "intent": "unknown",
                "params": {"original": user_input, "error": str(e)}
            }
    
    def translate_and_display(self, user_input):
        """Translate and print result (for testing)"""
        command = self.translate(user_input)
        print(f"You: {user_input}")
        print(f"STARK understands: {json.dumps(command, indent=2)}")
        return command

# Quick test
if __name__ == "__main__":
    translator = DeepSeekTranslator()
    
    print("DeepSeek Translator — Testing\n")
    test_phrases = [
        "set wallpaper.png as my background",
        "research artificial intelligence",
        "tell Sarah I'll be there in 5 minutes",
        "open Chrome",
        "can you please secure my system?"
    ]
    
    for phrase in test_phrases:
        translator.translate_and_display(phrase)
        print()
