from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio
import time

app = FastAPI(title="Real-Time Clinical Booking Agent (Local Test Mode)")

# Mock Database & State (In a real app, these would come from the other modules)
# We keep them here for the "Local Test Mode" convenience or import them correctly
from scheduler.appointment_engine.scheduler import AppointmentScheduler
from memory.session_memory.redis_client import MemoryManager
from agent.reasoning.agent import ReasoningAgent

scheduler = AppointmentScheduler()
memory = MemoryManager()
agent = ReasoningAgent()

def get_3_alternatives(date_str):
    return scheduler._get_3_alternatives(date_str)

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n[Server] Client connected.")
    
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            if payload.get("type") == "audio_chunk":
                if payload.get("detected_speech"):
                    print("[Server] Barge-in Detected! Interrupting current playback.")
                    await websocket.send_text(json.dumps({"type": "barge_in_ack"}))
                continue

            user_text = payload.get("text", "")
            print(f"[Server] Received Text: {user_text}")
            
            stt_ms = 120
            # Use the actual agent logic for reasoning
            intent_data, reasoning_ms = agent.process_intent(user_text)
            tts_ms = 100
            
            reply = "I understood your request."
            if intent_data.get("intent") == "bookAppointment":
                 reply = scheduler.book_appointment(
                     doctor_id=1, 
                     date_str=intent_data.get("date", "2023-11-01"),
                     requested_slot=intent_data.get("time", "10:00")
                 )
            elif intent_data.get("intent") == "checkAvailability":
                 slots = scheduler.check_availability(1, intent_data.get("date", "2023-11-01"))
                 reply = f"Available slots are: {', '.join(slots)}"

            total_ms = stt_ms + reasoning_ms + tts_ms
            print(f"--- Latency: STT {stt_ms}ms | Reasoning {reasoning_ms:.2f}ms | TTS {tts_ms}ms | Total {total_ms:.2f}ms ---")
            
            await websocket.send_text(json.dumps({
                "type": "audio_response",
                "text_reply": reply,
                "latency_metrics": {"total_ms": total_ms}
            }))

    except WebSocketDisconnect:
        print("[Server] Client disconnected.")
    except Exception as e:
        print(f"[Server] Error: {e}")
