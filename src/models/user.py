from enum import Enum

# // Enumeración con los posibles roles de usuario del sistema.
class UserRole(str, Enum):
    ADMIN = "admin"              # // Usuario administrador.
    VET = "vet"                  # // Usuario veterinario.
    RECEPTIONIST = "receptionist"  # // Usuario de recepción.

# // Clase que representa a un usuario del sistema.
class User:
    def __init__(self, id: int, username: str, password_hash: str, role: UserRole) -> None:
        # // Identificador único del usuario.
        self.id = id
        # // Nombre de usuario (login).
        self.username = username
        # // Hash de la contraseña (nunca se almacena la contraseña en claro).
        self.password_hash = password_hash
        # // Rol del usuario dentro del sistema (admin, vet, receptionist).
        self.role = role
