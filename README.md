# Real-Time Multilingual Voice AI Agent for Clinical Bookings

## System Architecture & Latency
This system is designed for real-time voice interactions to schedule clinical appointments. It features a latency budget of **< 450ms** optimized through the following pipeline:

- **User Speech** → **STT (Whisper/Deepgram)**: ~120ms
- **Language Detection & Reasoning (LLM)**: ~200ms
  - Powered by **Groq (Llama 3-70B)** or **GPT-4o-mini** to achieve blistering fast tool calling.
- **Tool Orchestration & Appointment Service**: ~30ms
- **TTS (Text-to-Speech)** → **Audio Response**: ~100ms

Total Latency: **< 450ms**

### Real-time Communication & Interrupt Handling (Barge-in)
The system uses **WebSockets** for true bi-directional audio streaming. 
**Barge-in logic**: The client streams audio chunks continuously. If the STT pipeline detects speech from the user while the TTS is currently playing an output, the system immediately aborts the ongoing TTS broadcast, flushes the audio queue, and prioritizes the new incoming intent.

## Memory Design
### Session Memory (Redis)
We use Redis to maintain real-time conversation state.
- Maps `session_id` to conversational `state` (e.g. `pending_intent`, `current_doctor`).
- **TTL Bonus**: We implement a Redis TTL (`redis.set(session_id, state, ex=3600)`) to ensure stale sessions expire, horizontally scaling our memory footprint.

### Persistent Memory (PostgreSQL)
We store core domain data safely using PostgreSQL.
- Includes `patient_id`, `preferred_language` (for auto-detecting English, Hindi, and Tamil), and `past_appointments`.

## Setup Instructions

1. **Install Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn websockets redis langchain openai groq psycopg2
   ```

3. **Run PostgreSQL and Redis**
   Ensure Redis and PostgreSQL are running locally or update the connection strings.
   Run the schema migration:
   ```bash
   psql -U postgres -d clinic_db -f database/schema.sql
   ```

4. **Environment Variables**
   Create a `.env` file with your API keys:
   ```env
   GROQ_API_KEY=your_groq_key
   REDIS_URL=redis://localhost:6379/0
   DB_URL=postgresql://user:password@localhost/clinic_db
   ```

5. **Start the FastAPI server**
   ```bash
   uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
   ```
