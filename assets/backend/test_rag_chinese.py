
import asyncio
import websockets
import json
import uuid

async def test_chat():
    task_id = str(uuid.uuid4())
    uri = f"ws://localhost:8000/ws/chat/{task_id}"
    
    # Chinese query matching the user's issue
    query = "h100是什么"
    
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected.")
            
            # Send the message
            message = {
                "message": query,
                "model": "gpt-oss-1.5b"
            }
            print(f"Sending message: {json.dumps(message)}")
            await websocket.send(json.dumps(message))
            
            # Listen for responses
            print("Waiting for response...")
            full_response = ""
            while True:
                response = await websocket.recv()
                try:
                    data = json.loads(response)
                    if data["type"] == "token":
                        print(f"Token: {data['data']}", end="", flush=True)
                        full_response += data['data']
                    elif data["type"] == "tool_start":
                        print(f"\n[Tool Start]: {data['name']} args={data['args']}")
                    elif data["type"] == "tool_end":
                        print(f"\n[Tool End]: {data['name']} result len={len(str(data.get('result', '')))}")
                    elif data["type"] == "node_end" and data["data"] == "generate":
                        print("\nGeneration finished.")
                        break
                    elif data["type"] == "error":
                        print(f"\nError: {data['data']}")
                        break
                except json.JSONDecodeError:
                    print(f"\nReceived raw: {response}")
                    
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat())
