from datetime import datetime
import sys
import os

# Mock data
mock_doctor_schedule = {
    "2023-11-01": ["10:00", "14:00"],
    "2023-11-02": ["09:00", "11:00"]
}
mock_valid_doctor_ids = [1, 2, 3]

class AppointmentScheduler:
    def __init__(self):
        self.booked_slots = mock_doctor_schedule
        self.valid_doctor_ids = mock_valid_doctor_ids

    def check_availability(self, doctor_id: int, date_str: str) -> list:
        booked = self.booked_slots.get(date_str, [])
        all_slots = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]
        return [slot for slot in all_slots if slot not in booked]

    def book_appointment(self, doctor_id: int, date_str: str, requested_slot: str) -> str:
        if doctor_id not in self.valid_doctor_ids:
            return "Invalid Doctor ID."

        try:
            req_datetime = datetime.strptime(f"{date_str} {requested_slot}", "%Y-%m-%d %H:%M")
            if req_datetime < datetime.now():
                return "Cannot book appointments in the past."
        except ValueError:
            pass 

        slots_for_date = self.booked_slots.get(date_str, [])
        if requested_slot in slots_for_date:
            alternatives = self._get_3_alternatives(date_str)
            alternatives_str = ", ".join(alternatives)
            return f"Slot already booked, suggest {alternatives_str} instead."
        
        self.booked_slots.setdefault(date_str, []).append(requested_slot)
        return "Booking successful."
        
    def _get_3_alternatives(self, date_str: str) -> list:
        booked = self.booked_slots.get(date_str, [])
        all_slots = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]
        available = [slot for slot in all_slots if slot not in booked]
        return available[:3] if len(available) >= 3 else available
