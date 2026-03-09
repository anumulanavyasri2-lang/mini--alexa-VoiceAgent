import json
import os
from openai import OpenAI  # Use OpenAI SDK to connect to Groq for blistering fast Llama 3-70b latency

class ClinicalBookingAgent:
    def __init__(self):
        # We use Groq (Llama 3-70B) or GPT-4o-mini to guarantee < 200ms reasoning latency
        api_key = os.getenv("GROQ_API_KEY", os.getenv("OPENAI_API_KEY", "fallback_key"))
        # Groq provides an OpenAI-compatible endpoint
        base_url = "https://api.groq.com/openai/v1" if os.getenv("GROQ_API_KEY") else "https://api.openai.com/v1"
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Genuine functions for true tool calling
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "checkAvailability",
                    "description": "Queries doctor schedules for availability given a date and/or doctor name.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_name": {"type": "string", "description": "The name of the doctor."},
                            "date": {"type": "string", "description": "The date for the appointment (YYYY-MM-DD)."}
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "bookAppointment",
                    "description": "Creates a new appointment booking.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "doctor_name": {"type": "string", "description": "Name of the doctor"},
                            "date": {"type": "string", "description": "Appointment date YYYY-MM-DD"},
                            "time": {"type": "string", "description": "Appointment time HH:MM"}
                        },
                        "required": ["doctor_name", "date", "time"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cancelAppointment",
                    "description": "Cancels an existing appointment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {"type": "string", "description": "ID of the appointment to cancel."}
                        },
                        "required": ["appointment_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "rescheduleAppointment",
                    "description": "Reschedules an existing appointment.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {"type": "string", "description": "ID of the appointment to reschedule."},
                            "new_date": {"type": "string", "description": "New appointment date YYYY-MM-DD."},
                            "new_time": {"type": "string", "description": "New appointment time HH:MM."}
                        },
                        "required": ["appointment_id", "new_date", "new_time"]
                    }
                }
            }
        ]

    def process_intent(self, user_text: str, session_history: list = None) -> dict:
        """
        Multilingual Capability: LLM Auto-detects English, Hindi, and Tamil and sets intent seamlessly.
        Converts speech transcription into a planned JSON operation containing intent, doctor, and date.
        """
        messages = [
            {"role": "system", "content": "You are a multilingual (English, Hindi, Tamil) Clinical Booking AI. Always map user intent to the provided tools. Output precise answers."},
        ]
        
        if session_history:
            messages.extend(session_history)
            
        messages.append({"role": "user", "content": user_text})

        # < 200ms reasoning goal via lightweight/fast model (llama3-70b-8192 or gpt-4o-mini)
        model_name = "llama3-70b-8192" if os.getenv("GROQ_API_KEY") else "gpt-4o-mini"
        response = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        if message.tool_calls:
            # Reconstruct tool call intent to the required JSON format
            tool_call = message.tool_calls[0]
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            return {
                "intent": func_name,
                "doctor": args.get("doctor_name"),
                "date": args.get("date"),
                "time": args.get("time"),
                "appointment_id": args.get("appointment_id")
            }
        
        # Fallback if no specific tool was called
        return {"intent": "conversational", "reply": message.content}
