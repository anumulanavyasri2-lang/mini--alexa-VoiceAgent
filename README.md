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
# Mini Alexa: AI-Powered Voice Assistant 🎤

## 📌 Project Overview
This project is a functional **Mini Alexa** voice assistant developed as part of the **2Care.ai** technical assignment. It is designed to demonstrate core competencies in **Speech Recognition**, **Natural Language Processing (NLP)**, and **Text-to-Speech (TTS)** integration using Python.

The assistant listens for user input via a microphone, processes the intent, and provides an automated voice response or executes a specific task.

---

## 🚀 Key Features
* **Voice Command Recognition:** Converts real-time human speech into text using the `SpeechRecognition` library.
* **Text-to-Speech (TTS) Engine:** Provides verbal feedback to the user via the `pyttsx3` or `gTTS` engine.
* **Dynamic Task Execution:** * Tells the current time and date.
    * Searches Wikipedia for instant information.
    * Opens popular websites like YouTube, Google, and Stack Overflow.
    * Plays music or YouTube videos directly from voice prompts.
* **Error Handling:** Gracefully manages background noise and unrecognized commands to ensure a smooth user experience.

---

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Libraries:** * `SpeechRecognition` (Audio Processing)
    * `pyttsx3` (Offline Text-to-Speech)
    * `PyAudio` (Microphone interface)
    * `Wikipedia` (Information retrieval)
    * `Webbrowser` (System browser control)

---

## 📽️ Demo Video
You can view the full screen recording of the project in action here:
👉 [**Watch the Demo on Google Drive**](https://drive.google.com/file/d/1YugL84FqlW_y0Qz8guj0Qd3htii1ti4H/view?usp=drivesdk)

---

## ⚙️ Setup & Installation
1.  **Clone the Repository:**
    ```bash
    git clone [INSERT_YOUR_GITHUB_LINK_HERE]
    ```
2.  **Install Dependencies:**
    ```bash
    pip install speechrecognition pyttsx3 pyaudio wikipedia
    ```
3.  **Run the Assistant:**
    ```bash
    python alexa_mini.py
    ```
