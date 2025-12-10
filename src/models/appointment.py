from datetime import datetime
from enum import Enum

# // Enumeración con los posibles estados de una cita veterinaria.
class AppointmentStatus(str, Enum):
    PENDING = "pending"      # // Cita pendiente de ser atendida.
    ATTENDED = "attended"    # // Cita que ya ha sido atendida.
    CANCELLED = "cancelled"  # // Cita que ha sido cancelada.

# // Clase que representa una cita veterinaria en el sistema.
class Appointment:
    def __init__(
        self,
        id: int,
        pet_id: int,
        vet_id: int,
        scheduled_at: datetime,
        reason: str,
        status: AppointmentStatus = AppointmentStatus.PENDING,
    ) -> None:
        # // Identificador único de la cita.
        self.id = id
        # // Identificador de la mascota a la que pertenece la cita.
        self.pet_id = pet_id
        # // Identificador del veterinario que atenderá la cita.
        self.vet_id = vet_id
        # // Fecha y hora programadas para la cita.
        self.scheduled_at = scheduled_at
        # // Motivo o descripción de la consulta.
        self.reason = reason
        # // Estado actual de la cita (por defecto: pendiente).
        self.status = status
