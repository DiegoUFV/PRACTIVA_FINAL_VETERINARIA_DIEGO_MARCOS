from src.db import Database

def test_add_medical_record():
    db = Database(":memory:")
    db.init_schema()

    db.execute(
        """
        INSERT INTO medical_records (pet_id, record_date, record_type, description)
        VALUES (1, '2025-01-01', 'Consulta', 'Revisión general')
        """
    )

    rows = db.query("SELECT * FROM medical_records")
    assert len(rows) == 1
