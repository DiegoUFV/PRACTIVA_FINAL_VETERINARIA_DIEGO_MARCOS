from src.db import Database

class ClientService:
    def __init__(self, db: Database):
        self.db = db

    def create_client(self, full_name: str, email: str, phone: str):
        self.db.execute(
            """
            INSERT INTO clients (full_name, email, phone)
            VALUES (?, ?, ?)
            """,
            (full_name, email, phone),
        )

    def list_clients(self):
        return self.db.query(
            "SELECT id, full_name, email, phone FROM clients"
        )

    def get_client_by_id(self, client_id: int):
        result = self.db.query(
            """
            SELECT id, full_name, email, phone
            FROM clients
            WHERE id = ?
            """,
            (client_id,)
        )
        return result[0] if result else None

    def find_by_name(self, name: str):
        return self.db.query(
            """
            SELECT id, full_name, email, phone
            FROM clients
            WHERE full_name LIKE ?
            """,
            (f"%{name}%",),
        )

    def update_client(self, client_id: int, name: str, email: str, phone: str):
        self.db.execute(
            """
            UPDATE clients
            SET full_name = ?, email = ?, phone = ?
            WHERE id = ?
            """,
            (name, email, phone, client_id)
        )

    def delete_client(self, client_id: int):
        self.db.execute(
            "DELETE FROM clients WHERE id = ?",
            (client_id,)
        )
