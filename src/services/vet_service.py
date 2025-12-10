from src.db import Database

class VetService:
    def __init__(self, db: Database):
        self.db = db

    def create_vet(self, full_name: str, specialty: str, schedule: str, email: str, phone: str):
        self.db.execute(
            """
            INSERT INTO vets (full_name, specialty, schedule, email, phone)
            VALUES (?, ?, ?, ?, ?)
            """,
            (full_name, specialty, schedule, email, phone),
        )

    def list_vets(self):
        return self.db.query(
            """
            SELECT id, full_name, specialty, schedule, email, phone
            FROM vets
            """
        )

    def get_vet_by_id(self, vet_id: int):
        rows = self.db.query(
            """
            SELECT id, full_name, specialty, schedule, email, phone
            FROM vets
            WHERE id = ?
            """,
            (vet_id,),
        )
        return rows[0] if rows else None

    def search_vets_by_name(self, name: str):
        return self.db.query(
            """
            SELECT id, full_name, specialty, schedule, email, phone
            FROM vets
            WHERE full_name LIKE ?
            """,
            (f"%{name}%",),
        )

    def update_vet(self, vet_id: int, full_name: str, specialty: str, schedule: str, email: str, phone: str):
        self.db.execute(
            """
            UPDATE vets
            SET full_name = ?, specialty = ?, schedule = ?, email = ?, phone = ?
            WHERE id = ?
            """,
            (full_name, specialty, schedule, email, phone, vet_id),
        )

    def delete_vet(self, vet_id: int):
        self.db.execute(
            "DELETE FROM vets WHERE id = ?", 
            (vet_id,),
        )
