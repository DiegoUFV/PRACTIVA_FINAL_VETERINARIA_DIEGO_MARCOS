from typing import List, Optional
from ..db import Database
from ..models import Client

class ClientService:
    """High-level operations for managing clients.

    Right now it uses very simple SQL; later we can refactor to repositories.
    """

    def __init__(self, db: Database) -> None:
        self.db = db

    def create_client(self, full_name: str, email: str, phone: str) -> None:
        self.db.execute(
            "INSERT INTO clients (full_name, email, phone) VALUES (?, ?, ?)",
            (full_name, email, phone),
        )

    def list_clients(self) -> list[tuple]:
        return self.db.query("SELECT id, full_name, email, phone FROM clients")

    def delete_client_if_no_pets(self, client_id: int) -> bool:
        pets = self.db.query("SELECT id FROM pets WHERE owner_id = ?", (client_id,))
        if pets:
            return False
        self.db.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        return True
