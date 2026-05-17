"""
Peter Daughter Agent
Handles research, studying, and information tasks
"""

import sys
import os
import requests
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Peter:
    def __init__(self):
        self.name = "Peter"
        self.kids = {
            "Karen": None,   # Summarizer (will add)
            "Ned": None,     # Quick facts
            "Miles": None    # Deep research
        }
    
    def handle_task(self, intent, params):
        """Route task to appropriate kid"""
        
        if intent == "research":
            topic = params.get("topic", "general")
            depth = params.get("depth", "summary")
            
            # Simple research using Wikipedia API
            try:
                # Search Wikipedia
                search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
                response = requests.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    summary = data.get('extract', 'No summary found')
                    title = data.get('title', topic)
                    
                    # Truncate if too long
                    if len(summary) > 500:
                        summary = summary[:500] + "..."
                    
                    return {
                        "status": "success",
                        "message": f"Here's what I found about {title}:\n{summary}"
                    }
                else:
                    # Try search as fallback
                    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={topic}&format=json"
                    response = requests.get(search_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        results = data.get('query', {}).get('search', [])
                        if results:
                            return {
                                "status": "success",
                                "message": f"Found these results for '{topic}':\n" + "\n".join([f"  - {r['title']}" for r in results[:3]])
                            }
                    
                    return {"status": "error", "message": f"Couldn't find information about '{topic}'"}
            
            except Exception as e:
                return {"status": "error", "message": f"Research failed: {str(e)}"}
        
        else:
            return {"status": "error", "message": f"Peter can't handle {intent}"}

if __name__ == "__main__":
    peter = Peter()
    result = peter.handle_task("research", {"topic": "artificial intelligence"})
    print(result)
