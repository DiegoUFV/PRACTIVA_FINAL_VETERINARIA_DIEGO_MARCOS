from typing import Optional

# // Clase que representa a un veterinario de la clínica.
class Vet:
    def __init__(
        self,
        id: int,
        full_name: str,
        specialty: Optional[str] = None,
        work_schedule: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> None:
        # // Identificador único del veterinario.
        self.id = id
        # // Nombre completo del veterinario.
        self.full_name = full_name
        # // Especialidad del veterinario (por ejemplo: cirugía, animales exóticos...).
        self.specialty = specialty
        # // Horario de trabajo (texto libre por ahora).
        self.work_schedule = work_schedule
        # // Correo electrónico profesional.
        self.email = email
        # // Teléfono de contacto.
        self.phone = phone
