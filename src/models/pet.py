from datetime import date
from typing import List, Optional
from .medical_record import MedicalRecordEntry

# // Clase que representa una mascota registrada en la clínica.
class Pet:
    def __init__(
        self,
        id: int,
        owner_id: int,
        name: str,
        species: str,
        breed: Optional[str] = None,
        sex: Optional[str] = None,
        birth_date: Optional[date] = None,
        medical_observations: Optional[str] = None,
        medical_history: Optional[List[MedicalRecordEntry]] = None,
    ) -> None:
        # // Identificador único de la mascota.
        self.id = id
        # // Identificador del cliente propietario de la mascota.
        self.owner_id = owner_id
        # // Nombre de la mascota.
        self.name = name
        # // Especie de la mascota (perro, gato, etc.).
        self.species = species
        # // Raza de la mascota (opcional).
        self.breed = breed
        # // Sexo de la mascota (opcional).
        self.sex = sex
        # // Fecha de nacimiento (opcional).
        self.birth_date = birth_date
        # // Observaciones médicas generales (opcional).
        self.medical_observations = medical_observations
        # // Historial médico de la mascota: lista de entradas de historia clínica.
        self.medical_history: List[MedicalRecordEntry] = medical_history if medical_history is not None else []

    def add_medical_entry(self, entry: MedicalRecordEntry) -> None:
        # // Añade una nueva entrada al historial médico de la mascota.
        self.medical_history.append(entry)
