from typing import List, Optional
from .pet import Pet

# Clase que representa a un cliente de la clínica veterinaria.
class Client:
    def __init__(self, id: int, full_name: str, email: str, phone: str, pets: Optional[List["Pet"]] = None) -> None:
        # Identificador único del cliente.
        self.id = id
        # Nombre completo del cliente.
        self.full_name = full_name
        # Correo electrónico del cliente.
        self.email = email
        # Teléfono de contacto del cliente.
        self.phone = phone
        # Si la viene una lista al almacena, si vienen None, inicializa una lista vacía.
        self.pets: List["Pet"] = pets if pets is not None else []

    def add_pet(self, pet: "Pet") -> None:
        # Añade una mascota a la lista de mascotas del cliente.
        self.pets.append(pet)

    def remove_pet(self, pet_id: int) -> None:
        #Elimina una mascota de la lista usando su identificador.
        self.pets = [p for p in self.pets if p.id != pet_id]

    def has_active_pets(self) -> bool:
        # Devuelve True si el cliente tiene al menos una mascota asociada.
        return len(self.pets) > 0
