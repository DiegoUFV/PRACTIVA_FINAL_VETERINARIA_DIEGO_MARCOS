from typing import List
from ..db import Database

class PetService:
    """Operations related to pets (mascotas)."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def create_pet(
        self,
        owner_id: int,
        name: str,
        species: str,
        breed: str | None = None,
        sex: str | None = None,
    ) -> None:
        self.db.execute(
            "INSERT INTO pets (owner_id, name, species, breed, sex) VALUES (?, ?, ?, ?, ?)",
            (owner_id, name, species, breed, sex),
        )

    def list_pets_by_client(self, client_id: int) -> list[tuple]:
        return self.db.query(
            "SELECT id, name, species, breed, sex FROM pets WHERE owner_id = ?",
            (client_id,),
        )
