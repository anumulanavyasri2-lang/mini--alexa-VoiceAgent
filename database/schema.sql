-- Database Schema for Clinical Appointments

-- Doctor Schedules (Availability)
CREATE TABLE IF NOT EXISTS doctor_schedule (
    id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL,
    available_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE,
    UNIQUE(doctor_id, available_date, start_time, end_time)
);

-- Past & Upcoming Appointments
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(255) NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(50) DEFAULT 'Scheduled', -- 'Scheduled', 'Cancelled', 'Rescheduled', 'Completed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast querying
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_schedule_doctor_date ON doctor_schedule(doctor_id, available_date);
