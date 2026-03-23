import sys, urllib.request, time
sys.path.insert(0, "src")
import os
os.environ["MCP_TEST_MODE"] = "true"
from mcp_feedback_enhanced.web.main import WebUIManager

manager = WebUIManager(port=8766)
manager.start_server()
time.sleep(2)
try:
    r = urllib.request.urlopen("http://127.0.0.1:8766/")
    print(f"HTTP {r.status} - OK!")
except Exception as e:
    print(f"Error: {e}")
