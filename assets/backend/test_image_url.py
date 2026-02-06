import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from tools.mcp_servers.image_understanding import explain_image

try:
    # A standard public image URL
    test_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    result = explain_image("What is in this image?", test_url)
    print(f"SUCCESS: {result}")
except Exception as e:
    print(f"FAILED: {e}")
