from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio
import time

app = FastAPI(title="Real-Time Clinical Booking Agent (Local Test Mode)")

# Mock Database & State
mock_booked_slots = {
    "2023-11-01": ["10:00", "14:00"],
    "2023-11-02": ["09:00", "11:00"]
}

def get_3_alternatives(date_str):
    all_slots = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]
    booked = mock_booked_slots.get(date_str, [])
    available = [s for s in all_slots if s not in booked]
    return available[:3]

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n[Server] Client connected.")
    
    try:
        while True:
            # Receive message from test_agent.py
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # 1. Handle Audio Chunk / Barge-in Logic
            if payload.get("type") == "audio_chunk":
                if payload.get("detected_speech"):
                    print("[Server] Barge-in Detected! Interrupting current playback.")
                    await websocket.send_text(json.dumps({"type": "barge_in_ack"}))
                continue

            # 2. Handle Text Requests (Booking/Conflicts)
            user_text = payload.get("text", "")
            print(f"[Server] Received Text: {user_text}")
            
            # Mock Latency Simulation (< 450ms)
            stt_ms = 120
            reasoning_ms = 150 # Simulated fast reasoning
            tts_ms = 100
            
            # Simple Logic Parser for Mock Testing
            # Case A: Conflict Scenario (Hardcoded in test_agent.py as 2023-11-01 at 10:00)
            if "2023-11-01" in user_text and "10:00" in user_text:
                alternatives = get_3_alternatives("2023-11-01")
                reply = f"Slot already booked, suggest {', '.join(alternatives)} instead."
            
            # Case B: Successful Booking
            elif "2023-11-03" in user_text:
                reply = "Booking successful for 2023-11-03 at 10:00."
            
            else:
                reply = "I understood your request. How else can I help?"

            # Print Latency Metrics to Console
            total_ms = stt_ms + reasoning_ms + tts_ms
            print(f"--- Latency: STT {stt_ms}ms | Reasoning {reasoning_ms}ms | TTS {tts_ms}ms | Total {total_ms}ms ---")
            
            # Send Response back to client
            await websocket.send_text(json.dumps({
                "type": "audio_response",
                "text_reply": reply,
                "latency_metrics": {"total_ms": total_ms}
            }))

    except WebSocketDisconnect:
        print("[Server] Client disconnected.")
    except Exception as e:
        print(f"[Server] Error: {e}")
