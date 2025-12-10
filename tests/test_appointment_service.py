from src.db import Database
from src.services import AppointmentService
from datetime import datetime

def test_create_appointment():
    db = Database(":memory:")
    db.init_schema()
    service = AppointmentService(db)

    service.create_appointment(
        pet_id=1,
        vet_id=1,
        scheduled_at=datetime(2025, 1, 1, 10, 0),
        reason="Revisión"
    )

    rows = db.query("SELECT * FROM appointments")
    assert len(rows) == 1

def test_list_appointments_by_date():
    db = Database(":memory:")
    db.init_schema()
    service = AppointmentService(db)

    service.create_appointment(1, 1, datetime(2025,1,1,10,0), "Rev")
    result = service.list_appointments_by_date("2025-01-01")

    assert len(result) == 1
