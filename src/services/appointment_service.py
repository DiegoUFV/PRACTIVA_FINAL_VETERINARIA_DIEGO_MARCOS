from datetime import datetime
from ..db import Database
from ..models import AppointmentStatus

class AppointmentService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create_appointment(
        self,
        pet_id: int,
        vet_id: int,
        scheduled_at: datetime,
        reason: str,
    ) -> None:
        """Create a new appointment in the database.

        We store `scheduled_at` as an ISO-formatted string so that it is easy
        to filter by date using simple LIKE queries.
        """
        self.db.execute(
            """
            INSERT INTO appointments (pet_id, vet_id, scheduled_at, reason, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (pet_id, vet_id, scheduled_at.isoformat(), reason, AppointmentStatus.PENDING.value),
        )

    def list_appointments_by_date(self, date_str: str) -> list[tuple]:
        # Very naive filter for the day using LIKE on the ISO date prefix
        return self.db.query(
            """
            SELECT id, pet_id, vet_id, scheduled_at, reason, status
            FROM appointments
            WHERE scheduled_at LIKE ?
            ORDER BY scheduled_at
            """,
            (f"{date_str}%",),
        )

    def update_status(self, appointment_id: int, status: AppointmentStatus) -> None:
        self.db.execute(
            "UPDATE appointments SET status = ? WHERE id = ?",
            (status.value, appointment_id),
        )
