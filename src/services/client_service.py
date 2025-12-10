from ..db import Database

# Servicio encargado de las operaciones relacionadas con clientes.
class ClientService:
    def __init__(self, db: Database) -> None:
        # Instancia de base de datos para realizar operaciones SQL.
        self.db = db

    # Crea un nuevo cliente en la base de datos.
    def create_client(self, full_name: str, email: str, phone: str) -> None:
        self.db.execute(
            """
            INSERT INTO clients (full_name, email, phone)
            VALUES (?, ?, ?)
            """,
            (full_name, email, phone),
        )

    # Devuelve todos los clientes registrados.
    def list_clients(self) -> list[tuple]:
        return self.db.query(
            "SELECT id, full_name, email, phone FROM clients"
        )

    # Elimina un cliente solo si no tiene mascotas asociadas.
    def delete_client_if_no_pets(self, client_id: int) -> bool:
        pets = self.db.query(
            "SELECT id FROM pets WHERE owner_id = ?",
            (client_id,),
        )

        # Si tiene mascotas, no se puede borrar.
        if pets:
            return False

        # Si no tiene mascotas, se elimina el cliente.
        self.db.execute("DELETE FROM clients WHERE id = ?", (client_id,))
        return True
