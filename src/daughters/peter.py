"""
Peter Daughter Agent - Fixed Wikipedia search
"""

import sys
import os
import requests
import urllib.parse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Peter:
    def __init__(self):
        self.name = "Peter"
    
    def handle_task(self, intent, params):
        if intent == "research":
            topic = params.get("topic", "general")
            return self._simple_wikipedia(topic)
        else:
            return {"status": "error", "message": f"Peter can't handle {intent}"}
    
    def _simple_wikipedia(self, query):
        """Use Simple English Wikipedia for better success rate"""
        try:
            # Try Simple English Wikipedia first (more reliable)
            encoded = urllib.parse.quote(query.replace(' ', '_'))
            url = f"https://simple.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            
            response = requests.get(url, timeout=15, headers={'User-Agent': 'STARK-Agent/1.0'})
            
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', query)
                summary = data.get('extract', '')
                
                if summary:
                    if len(summary) > 800:
                        summary = summary[:800] + "..."
                    return {
                        "status": "success",
                        "message": f"📚 {title}\n\n{summary}"
                    }
            
            # Fallback: Use DuckDuckGo API (no key required)
            ddg_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(ddg_url, timeout=15, headers={'User-Agent': 'STARK-Agent/1.0'})
            
            if response.status_code == 200:
                data = response.json()
                abstract = data.get('Abstract', '')
                if abstract:
                    if len(abstract) > 800:
                        abstract = abstract[:800] + "..."
                    return {
                        "status": "success",
                        "message": f"🔍 {query}\n\n{abstract}"
                    }
            
            return {
                "status": "error",
                "message": f"Couldn't find information about '{query}'. Try a different term."
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Search error: {str(e)}"}

if __name__ == "__main__":
    peter = Peter()
    test = peter.handle_task("research", {"topic": "quantum computing"})
    print(test)
