from src.models import Invoice, InvoiceLine, InvoiceStatus
from datetime import datetime

def test_invoice_line_total():
    line = InvoiceLine("Consulta", 2, 30.0)
    assert line.total == 60.0

def test_invoice_totals():
    inv = Invoice(
        id=1,
        client_id=1,
        pet_id=1,
        appointment_id=1,
        created_at=datetime.now(),
    )

    inv.add_line(InvoiceLine("Vacuna", 1, 20))
    inv.add_line(InvoiceLine("Consulta", 1, 30))

    assert inv.subtotal == 50
    assert inv.vat_amount == 50 * 0.21
    assert inv.total == inv.subtotal + inv.vat_amount

def test_invoice_status_default():
    inv = Invoice(
        id=1,
        client_id=1,
        pet_id=1,
        appointment_id=1,
        created_at=datetime.now(),
    )
    assert inv.status == InvoiceStatus.DRAFT
