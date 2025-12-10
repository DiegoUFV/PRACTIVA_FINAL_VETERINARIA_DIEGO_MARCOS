from datetime import datetime
from ..models import Invoice, InvoiceLine, InvoiceStatus

class BillingService:
    """For now this is an in-memory placeholder; we can persist to DB later."""

    def __init__(self) -> None:
        self._invoices: dict[int, Invoice] = {}
        self._next_id = 1

    def create_invoice(
        self,
        client_id: int,
        pet_id: int,
        appointment_id: int,
    ) -> Invoice:
        invoice = Invoice(
            id=self._next_id,
            client_id=client_id,
            pet_id=pet_id,
            appointment_id=appointment_id,
            issue_date=datetime.now(),
        )
        self._invoices[self._next_id] = invoice
        self._next_id += 1
        return invoice

    def add_line(self, invoice_id: int, description: str, quantity: float, unit_price: float) -> None:
        invoice = self._invoices[invoice_id]
        invoice.add_line(InvoiceLine(description=description, quantity=quantity, unit_price=unit_price))

    def get_invoice(self, invoice_id: int) -> Invoice:
        return self._invoices[invoice_id]

    def mark_paid(self, invoice_id: int) -> None:
        self._invoices[invoice_id].status = InvoiceStatus.PAID
