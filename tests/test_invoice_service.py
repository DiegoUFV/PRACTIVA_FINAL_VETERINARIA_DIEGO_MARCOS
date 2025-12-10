from src.db import Database
from datetime import datetime

def test_create_invoice_db():
    db = Database(":memory:")
    db.init_schema()

    db.execute(
        "INSERT INTO invoices (client_id, pet_id, appointment_id, created_at, status) VALUES (1,1,1,?,?)",
        (datetime.now().isoformat(), "draft"),
    )

    result = db.query("SELECT * FROM invoices")
    assert len(result) == 1

def test_add_invoice_line_db():
    db = Database(":memory:")
    db.init_schema()

    db.execute("INSERT INTO invoices (client_id, pet_id, appointment_id, created_at, status) VALUES (1,1,1,'2025','draft')")
    invoice_id = db.query("SELECT last_insert_rowid()")[0][0]

    db.execute("INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price) VALUES (?,?,?,?)",
               (invoice_id, "Consulta", 1, 30.0))

    rows = db.query("SELECT * FROM invoice_lines")
    assert len(rows) == 1
