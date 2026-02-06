import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from tools.mcp_servers.rag import fetch_web_content

async def test_web():
    try:
        url = "https://www.google.com/search?q=NVIDIA+H100"
        result = await fetch_web_content(url)
        print(f"SUCCESS (length {len(result)}): {result[:200]}...")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_web())
