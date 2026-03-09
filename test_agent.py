import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/stream"
    try:
        async with websockets.connect(uri) as websocket:
            
            # Test 1: Successful Booking
            success_payload = {
                "type": "text",
                "text": "Book an appointment for a cardiologist on 2023-11-03 at 10:00"
            }
            print(f"\n[Test Script] Sending Successful Booking Request...")
            await websocket.send(json.dumps(success_payload))
            response = await websocket.recv()
            print(f"[Test Script] Received: {json.loads(response).get('text_reply')}")
            
            # Test 2: Conflict Scenario (10:00 on 2023-11-01 is taken)
            conflict_payload = {
                "type": "text",
                "text": "Book an appointment for 2023-11-01 at 10:00"
            }
            print(f"\n[Test Script] Sending Conflict Scenario Request...")
            await websocket.send(json.dumps(conflict_payload))
            response = await websocket.recv()
            print(f"[Test Script] Received: {json.loads(response).get('text_reply')}")
            
            # Test 3: Barge-in logic
            barge_in_payload = {
                "type": "audio_chunk",
                "detected_speech": True
            }
            print(f"\n[Test Script] Sending Barge-in Request...")
            await websocket.send(json.dumps(barge_in_payload))
            response = await websocket.recv()
            print(f"[Test Script] Received Barge-in ACK: {json.loads(response).get('type')}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
