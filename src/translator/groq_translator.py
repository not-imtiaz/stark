"""
Groq Translator — Fixed for app names
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqTranslator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.system_prompt = """
You are STARK's translator. Convert human commands into JSON machine language.
Output ONLY valid JSON. No explanation. No extra text.

Possible intents:
- set_wallpaper : change desktop background
- research : search for information
- send_message : send a message
- open_app : launch an application (IMPORTANT: extract the app name)
- defend : security tasks
- get_time : current time
- unknown : if you cannot understand

CRITICAL for open_app: Always extract the application name into the "app" field.
Examples:
"open Firefox" → {"intent": "open_app", "params": {"app": "firefox"}}
"launch Chrome" → {"intent": "open_app", "params": {"app": "chrome"}}
"start terminal" → {"intent": "open_app", "params": {"app": "terminal"}}

Example for set_wallpaper:
"set wallpaper.png as background" → {"intent": "set_wallpaper", "params": {"file": "wallpaper.png"}}

Example for research:
"research quantum computing" → {"intent": "research", "params": {"topic": "quantum computing"}}

Example for send_message:
"tell Tony I'm late" → {"intent": "send_message", "params": {"recipient": "Tony", "content": "I'm late"}}

Example for get_time:
"what time is it" → {"intent": "get_time", "params": {}}

Example for unknown:
"what is the weather" → {"intent": "unknown", "params": {"original": "what is the weather"}}
"""
    
    def translate(self, user_input):
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"intent": "unknown", "params": {"original": user_input, "error": str(e)}}
    
    def translate_and_display(self, user_input):
        command = self.translate(user_input)
        print(f"You: {user_input}")
        print(f"STARK understands: {json.dumps(command, indent=2)}")
        return command

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not found")
    else:
        translator = GroqTranslator()
        test_phrases = [
            "open Firefox",
            "launch Chrome",
            "tell Sarah I'm late",
            "what time is it"
        ]
        for phrase in test_phrases:
            translator.translate_and_display(phrase)
            print()
