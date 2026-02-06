
import asyncio
import websockets
import json
import uuid

async def test_rag():
    chat_id = str(uuid.uuid4())
    uri = f"ws://localhost:8000/ws/chat/{chat_id}"
    
    print(f"Connecting to {uri}")
    async with websockets.connect(uri) as websocket:
        # Receive history
        response = await websocket.recv()
        print(f"Received history: {response}")
        
        # Send query
        msg = {
            "message": "Use the search_knowledge_base tool to find out what is the H100 GPU",
            "image_id": None
        }
        await websocket.send(json.dumps(msg))
        print(f"Sent: {msg['message']}")
        
        # Listen for response
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                # print(f"Received: {data}")
                
                if isinstance(data, dict):
                    print(f"Received dict: {data}")
                    if data.get("type") == "tool_start":
                        print(f"Tool started: {data.get('data')}")
                        if data.get("data") == "search_knowledge_base":
                             print("SUCCESS: RAG Tool triggered!")
                             # Don't return, let it finish to see full output
                             
                    if data.get("type") == "error":
                        print(f"Error: {data}")
                        return
                else:
                    # It's a token string
                    print(f"Token: {data}", end="", flush=True)
                    
            except Exception as e:
                print(f"Error reading: {e}")
                break

if __name__ == "__main__":
    asyncio.run(test_rag())
