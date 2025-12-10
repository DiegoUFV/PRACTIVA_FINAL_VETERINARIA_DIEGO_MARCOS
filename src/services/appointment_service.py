from datetime import datetime
from ..db import Database
from ..models import AppointmentStatus

# Servicio encargado de gestionar las citas veterinarias.
class AppointmentService:
    def __init__(self, db: Database) -> None:
        # Guardamos la instancia de la base de datos para usarla en los métodos.
        self.db = db

    # Crea una nueva cita en la base de datos.
    def create_appointment(
        self,
        pet_id: int,              # ID de la mascota relacionada con la cita.
        vet_id: int,              # ID del veterinario asignado.
        scheduled_at: datetime,   # Fecha y hora de la cita.
        reason: str,              # Motivo de la consulta.
    ) -> None:

        # Guardamos scheduled_at en formato ISO para facilitar búsquedas por fecha.
        self.db.execute(
            """
            INSERT INTO appointments (pet_id, vet_id, scheduled_at, reason, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                pet_id,
                vet_id,
                scheduled_at.isoformat(),
                reason,
                AppointmentStatus.PENDING.value,   # Estado inicial: "pending".
            ),
        )

    # Lista todas las citas de un día concreto.
    def list_appointments_by_date(self, date_str: str) -> list[tuple]:
        # Se usa LIKE con "YYYY-MM-DD%" para obtener todas las citas del día.
        return self.db.query(
            """
            SELECT id, pet_id, vet_id, scheduled_at, reason, status
            FROM appointments
            WHERE scheduled_at LIKE ?
            ORDER BY scheduled_at
            """,
            (f"{date_str}%",),
        )

    # Actualiza el estado de una cita.
    def update_status(self, appointment_id: int, status: AppointmentStatus) -> None:
        self.db.execute(
            "UPDATE appointments SET status = ? WHERE id = ?",
            (status.value, appointment_id),   # status.value = string del Enum.
        )
