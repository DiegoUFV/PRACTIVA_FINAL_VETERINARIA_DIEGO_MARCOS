from src.db import Database

class AppointmentService:
    def __init__(self, db: Database):
        self.db = db

    def create_appointment(self, pet_id: int, vet_id: int, scheduled_at: str, reason: str):
        self.db.execute(
            """
            INSERT INTO appointments (pet_id, vet_id, scheduled_at, reason, status)
            VALUES (?, ?, ?, ?, 'PENDING')
            """,
            (pet_id, vet_id, scheduled_at, reason),
        )

    def list_appointments_by_date(self, date_str: str):
        return self.db.query(
            """
            SELECT id, pet_id, vet_id, scheduled_at, reason, status
            FROM appointments
            WHERE DATE(scheduled_at) = ?
            ORDER BY scheduled_at ASC
            """,
            (date_str,),
        )

    def get_appointment_by_id(self, appointment_id: int):
        rows = self.db.query(
            """
            SELECT id, pet_id, vet_id, scheduled_at, reason, status
            FROM appointments
            WHERE id = ?
            """,
            (appointment_id,),
        )
        return rows[0] if rows else None

    def update_appointment(self, appointment_id: int, new_datetime: str, new_reason: str):
        self.db.execute(
            """
            UPDATE appointments
            SET scheduled_at = ?, reason = ?
            WHERE id = ?
            """,
            (new_datetime, new_reason, appointment_id),
        )

    def update_status(self, appointment_id: int, new_status: str):
        self.db.execute(
            """
            UPDATE appointments
            SET status = ?
            WHERE id = ?
            """,
            (new_status, appointment_id),
        )
