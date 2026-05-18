"""
Peter Daughter Agent - Returns both summary (for voice) and full text (for dashboard)
"""

import sys
import os
import requests
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Peter:
    def __init__(self):
        self.name = "Peter"
    
    def handle_task(self, intent, params):
        if intent == "research":
            topic = params.get("topic", "general")
            return self._smart_research(topic)
        else:
            return {"status": "error", "message": f"Peter can't handle {intent}"}
    
    def _smart_research(self, query):
        """Research and return both summary (voice) and full text (dashboard)"""
        try:
            encoded = urllib.parse.quote(query.replace(' ', '_'))
            url = f"https://simple.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            
            response = requests.get(url, timeout=15, headers={'User-Agent': 'STARK-Agent/1.0'})
            
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', query)
                full_text = data.get('extract', 'No information found.')
                
                # Create summary (first 3 sentences or 300 characters)
                summary = self._create_summary(full_text)
                
                return {
                    "status": "success",
                    "summary": summary,  # For voice
                    "full_text": full_text,  # For dashboard
                    "title": title,
                    "source": "Wikipedia"
                }
            
            # Fallback to DuckDuckGo
            ddg_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
            response = requests.get(ddg_url, timeout=15, headers={'User-Agent': 'STARK-Agent/1.0'})
            
            if response.status_code == 200:
                data = response.json()
                full_text = data.get('Abstract', 'No information found.')
                summary = self._create_summary(full_text)
                
                return {
                    "status": "success",
                    "summary": summary,
                    "full_text": full_text,
                    "title": query,
                    "source": "DuckDuckGo"
                }
            
            return {
                "status": "error",
                "message": f"Couldn't find information about '{query}'"
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Research error: {str(e)}"}
    
    def _create_summary(self, text, max_sentences=2, max_chars=300):
        """Create a short summary for voice output"""
        if not text:
            return "No information available."
        
        # Split into sentences
        sentences = text.replace('\n', ' ').split('. ')
        summary_sentences = sentences[:max_sentences]
        summary = '. '.join(summary_sentences)
        
        if len(summary) > max_chars:
            summary = summary[:max_chars] + "..."
        
        return summary

if __name__ == "__main__":
    peter = Peter()
    result = peter.handle_task("research", {"topic": "quantum computing"})
    print(f"Summary (for voice): {result.get('summary')}")
    print(f"\nFull text (for dashboard): {result.get('full_text')[:200]}...")
    def get_kids(self):
        return ["Karen", "Ned", "Miles"]
