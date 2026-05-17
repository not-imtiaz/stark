"""
Groq Translator — Fast, free LLM translation for STARK
No credit card required. 14,400 requests/day free.
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

Possible intents: set_wallpaper, research, send_message, code, defend, open_app, unknown

Examples:
Input: "set wallpaper.png as my background"
Output: {"intent": "set_wallpaper", "params": {"file": "wallpaper.png"}}

Input: "research quantum computing"
Output: {"intent": "research", "params": {"topic": "quantum computing", "depth": "summary"}}

Input: "tell Tony I'm late"
Output: {"intent": "send_message", "params": {"recipient": "Tony", "content": "I'm late", "platform": "whatsapp"}}

If unknown: {"intent": "unknown", "params": {"original": "user input"}}
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
        print("ERROR: GROQ_API_KEY not found in .env")
        print("Get one at: console.groq.com")
    else:
        translator = GroqTranslator()
        test_phrases = [
            "set wallpaper.png as my background",
            "research artificial intelligence",
            "tell Sarah I'll be there"
        ]
        for phrase in test_phrases:
            translator.translate_and_display(phrase)
            print()
