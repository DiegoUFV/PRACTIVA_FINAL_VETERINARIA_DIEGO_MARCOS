from datetime import datetime, date
from typing import Optional

# Clase que representa una entrada básica en la historia clínica.
class MedicalRecordEntry:
    def __init__(
        self,
        id: int,
        pet_id: int,
        created_at: datetime,
        vet_id: int,
        diagnosis: str,
        notes: str,
    ) -> None:
        # Identificador único de la entrada de historia clínica.
        self.id = id
        # Identificador de la mascota a la que pertenece esta entrada.
        self.pet_id = pet_id
        # Fecha y hora de creación de la entrada.
        self.created_at = created_at
        # Identificador del veterinario que registró la entrada.
        self.vet_id = vet_id
        # Diagnóstico principal asociado a la visita.
        self.diagnosis = diagnosis
        # Notas adicionales o comentarios del veterinario.
        self.notes = notes

# Clase que representa un tratamiento prescrito a una mascota.
class Treatment:
    def __init__(
        self,
        id: int,
        pet_id: int,
        vet_id: int,
        start_date: date,
        end_date: Optional[date],
        description: str,
        medication: Optional[str] = None,
        dosage: Optional[str] = None,
    ) -> None:
        # Identificador único del tratamiento.
        self.id = id
        # Identificador de la mascota tratada.
        self.pet_id = pet_id
        # Identificador del veterinario responsable del tratamiento.
        self.vet_id = vet_id
        # Fecha de inicio del tratamiento.
        self.start_date = start_date
        # Fecha de fin del tratamiento (opcional).
        self.end_date = end_date
        # Descripción general del tratamiento.
        self.description = description
        # Medicación asociada al tratamiento (opcional).
        self.medication = medication
        # Posología o dosis de la medicación (opcional).
        self.dosage = dosage

# Clase que representa una vacuna administrada a una mascota.
class Vaccination:
    def __init__(
        self,
        id: int,
        pet_id: int,
        vaccine_name: str,
        administered_at: date,
        next_due_date: Optional[date] = None,
    ) -> None:
        # Identificador único del registro de vacunación.
        self.id = id
        # Identificador de la mascota vacunada.
        self.pet_id = pet_id
        # Nombre de la vacuna administrada.
        self.vaccine_name = vaccine_name
        # Fecha en la que se administró la vacuna.
        self.administered_at = administered_at
        # Fecha recomendada para la próxima dosis (opcional).
        self.next_due_date = next_due_date
