from ..db import Database

# Servicio que proporciona datos básicos para informes y estadísticas.
class ReportingService:
    def __init__(self, db: Database) -> None:
        # Instancia de base de datos para consultas.
        self.db = db

    # Cuenta cuántos clientes hay registrados.
    def count_clients(self) -> int:
        result = self.db.query("SELECT COUNT(*) FROM clients")
        return result[0][0]

    # Cuenta cuántas mascotas hay registradas.
    def count_pets(self) -> int:
        result = self.db.query("SELECT COUNT(*) FROM pets")
        return result[0][0]

    # Cuenta cuántas citas existen.
    def count_appointments(self) -> int:
        result = self.db.query("SELECT COUNT(*) FROM appointments")
        return result[0][0]
