import sqlite3
from pathlib import Path
from typing import Any, Iterable

class Database:
    """Very small wrapper around SQLite.

    For this practice we keep it intentionally simple:
    * a single SQLite file on disk
    * a helper to initialise the minimal schema we need
    * small helpers to execute and query SQL.
    """

    def __init__(self, path: str = "clinic_vet.db") -> None:
        self.db_path = Path(path)

    def connect(self) -> sqlite3.Connection:
        # `check_same_thread=False` allows reuse from Streamlit reruns if needed
        return sqlite3.connect(self.db_path, check_same_thread=False)

    # --- Schema management -------------------------------------------------

    def init_schema(self) -> None:
        """Create the basic tables if they do not exist.

        The goal is not to model the whole clinic here, just enough for the
        pages included in this skeleton:
        * clients
        * pets
        * appointments
        """
        conn = self.connect()
        cur = conn.cursor()

        # Clients table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT,
                phone TEXT
            )
            """
        )

        # Pets table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT,
                sex TEXT,
                FOREIGN KEY (owner_id) REFERENCES clients(id)
            )
            """
        )

        # Appointments table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER NOT NULL,
                vet_id INTEGER,
                scheduled_at TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (pet_id) REFERENCES pets(id)
            )
            """
        )
                    # Tabla sencilla de historia clínica
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER NOT NULL,
                record_date TEXT NOT NULL,
                record_type TEXT NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (pet_id) REFERENCES pets(id)
            )
            """
        )
        

        conn.commit()
        conn.close()

    # --- Small helpers -----------------------------------------------------

    def execute(self, sql: str, params: Iterable[Any] = ()) -> None:
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        conn.close()

    def query(self, sql: str, params: Iterable[Any] = ()) -> list[tuple]:
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.close()
        return rows
