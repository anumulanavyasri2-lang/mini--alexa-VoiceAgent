class LatencyLogger:
    def __init__(self):
        self.stt_latency = 0.0
        self.reasoning_latency = 0.0
        self.tts_latency = 0.0

    def log_stt(self, latency_ms: float):
        self.stt_latency = latency_ms

    def log_reasoning(self, latency_ms: float):
        self.reasoning_latency = latency_ms

    def log_tts(self, latency_ms: float):
        self.tts_latency = latency_ms

    def print_metrics(self):
        total_latency = self.stt_latency + self.reasoning_latency + self.tts_latency
        print(f"\n--- Latency Breakdown ---")
        print(f"STT Latency:       {self.stt_latency:.2f}ms")
        print(f"Reasoning Latency: {self.reasoning_latency:.2f}ms")
        print(f"TTS Latency:       {self.tts_latency:.2f}ms")
        print(f"Total Latency:     {total_latency:.2f}ms")
        if total_latency < 450:
            print("SUCCESS: Total Latency is < 450ms")
        else:
            print("WARNING: Total Latency exceeded 450ms budget")
        print("-------------------------\n")
        return total_latency
