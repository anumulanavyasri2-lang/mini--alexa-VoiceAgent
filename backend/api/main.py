from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json

app = FastAPI(title="Real-Time Clinical Booking Agent", version="1.0.0")

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint handling real-time audio streams.
    Latency budget: STT (120ms) + Reasoning (200ms) + TTS (100ms) = < 450ms.
    """
    await websocket.accept()
    session_id = websocket.headers.get("Sec-WebSocket-Key", "default-session")
    
    try:
        while True:
            # 1. Receiver audio from user iteratively
            data = await websocket.receive_text() # Receiving JSON wrapper for audio payload or binary chunks
            payload = json.loads(data)
            
            # 2. Check for "Barge-in" logic (user interrupting the agent)
            if payload.get("type") == "audio_chunk":
               if payload.get("detected_speech"):
                   # Trigger "Barge-in" -> immediately halt ongoing TTS synthesis/broadcast in the pipeline
                   print("Barge-in detected! Halting current TTS audio response immediately.")
                   # Logic to flush the TTS queue goes here
            
            # STT -> LLM Reasoning -> TTS mock pipeline invocation
            # In a real deployed setup, this integrates Whisper/Deepgram STT, OpenAI/Groq Tool Calling, and TTS concurrently
            response_json = {
               "type": "audio_response",
               "audio_data": "base64_encoded_audio_bytes_mock"
            }
            await websocket.send_text(json.dumps(response_json))
            
    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")
