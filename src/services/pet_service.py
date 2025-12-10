from src.db import Database

class PetService:
    def __init__(self, db: Database):
        self.db = db

    def create_pet(self, owner_id: int, name: str, species: str, breed: str, sex: str):
        self.db.execute(
            """
            INSERT INTO pets (owner_id, name, species, breed, sex)
            VALUES (?, ?, ?, ?, ?)
            """,
            (owner_id, name, species, breed, sex)
        )

    def get_pet_by_id(self, pet_id: int):
        rows = self.db.query(
            "SELECT id, owner_id, name, species, breed, sex FROM pets WHERE id = ?",
            (pet_id,),
        )
        return rows[0] if rows else None

    def update_pet(self, pet_id: int, name: str, species: str, breed: str, sex: str):
        self.db.execute(
            """
            UPDATE pets
            SET name = ?, species = ?, breed = ?, sex = ?
            WHERE id = ?
            """,
            (name, species, breed, sex, pet_id)
        )

    def delete_pet(self, pet_id: int):
        self.db.execute("DELETE FROM pets WHERE id = ?", (pet_id,))

        
    def list_pets_by_client(self, client_id: int) -> list[tuple]:
        return self.db.query(
            """
            SELECT id, name, species, breed, sex
            FROM pets
            WHERE owner_id = ?
            """,
            (client_id,),
        )
