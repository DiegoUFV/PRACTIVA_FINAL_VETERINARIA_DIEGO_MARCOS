from ..db import Database

class ReportingService:
    """Generate simple statistics and reports.

    We will implement proper reporting later; now just placeholders.
    """

    def __init__(self, db: Database) -> None:
        self.db = db

    def count_clients(self) -> int:
        rows = self.db.query("SELECT COUNT(*) FROM clients")
        return int(rows[0][0]) if rows else 0

    def count_pets(self) -> int:
        rows = self.db.query("SELECT COUNT(*) FROM pets")
        return int(rows[0][0]) if rows else 0

    def count_appointments(self) -> int:
        rows = self.db.query("SELECT COUNT(*) FROM appointments")
        return int(rows[0][0]) if rows else 0
