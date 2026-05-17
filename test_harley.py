import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from daughters.harley import Harley

h = Harley()
result = h.handle_task('open_app', {'app': 'firefox'})
print(result)
