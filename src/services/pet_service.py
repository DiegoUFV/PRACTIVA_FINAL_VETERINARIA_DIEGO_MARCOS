from ..db import Database

# Servicio para gestionar mascotas.
class PetService:
    def __init__(self, db: Database) -> None:
        # Instancia de la base de datos.
        self.db = db

    # Crea una nueva mascota asociada a un cliente.
    def create_pet(
        self,
        owner_id: int,
        name: str,
        species: str,
        breed: str,
        sex: str,
    ) -> None:
        self.db.execute(
            """
            INSERT INTO pets (owner_id, name, species, breed, sex)
            VALUES (?, ?, ?, ?, ?)
            """,
            (owner_id, name, species, breed, sex),
        )

    # Lista todas las mascotas pertenecientes a un cliente.
    def list_pets_by_client(self, client_id: int) -> list[tuple]:
        return self.db.query(
            """
            SELECT id, name, species, breed, sex
            FROM pets
            WHERE owner_id = ?
            """,
            (client_id,),
        )
