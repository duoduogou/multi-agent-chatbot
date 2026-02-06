
import asyncio
import websockets
import json
import uuid
import httpx

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/chat"

async def set_sources(sources):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/selected_sources", json=sources)
        print(f"Set sources to {sources}: {response.status_code}")

async def test_query(query, description):
    task_id = str(uuid.uuid4())
    uri = f"{WS_URL}/{task_id}"
    
    print(f"\n--- Testing: {description} ---")
    print(f"Connecting to {uri}...")
    
    full_response = ""
    try:
        async with websockets.connect(uri) as websocket:
            # Send message with 120b model
            message = {
                "message": query,
                "model": "gpt-oss-120b"
            }
            print(f"Sending: {json.dumps(message)}")
            await websocket.send(json.dumps(message))
            
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                
                if data["type"] == "token":
                    print(data['data'], end="", flush=True)
                    full_response += data['data']
                elif data["type"] == "node_end" and data["data"] == "generate":
                    print("\nGeneration finished.")
                    break
                elif data["type"] == "error":
                    print(f"\nError: {data['data']}")
                    break
    except Exception as e:
        print(f"Error: {e}")
        
    return full_response

async def run_tests():
    # TEST 1: STRICT SELECTION - Sources Selected -> RAG SHOULD RUN
    await set_sources(["NVIDIA H100 GPU.pdf"])
    # Give a moment for config to persist if needed
    await asyncio.sleep(1)
    
    print("\n[TEST 1] Query with source selected (Expect RAG)")
    await test_query("h100是什么", "With Source")

    # TEST 2: STRICT SELECTION - No Sources -> RAG SHOULD NOT RUN
    await set_sources([])
    await asyncio.sleep(1)
    
    print("\n[TEST 2] Query with NO source selected (Expect NO RAG)")
    await test_query("h100是什么", "Without Source")

if __name__ == "__main__":
    asyncio.run(run_tests())
