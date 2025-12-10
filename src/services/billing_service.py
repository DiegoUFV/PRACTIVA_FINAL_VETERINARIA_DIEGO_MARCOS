from datetime import datetime
from ..models import Invoice, InvoiceLine, InvoiceStatus

# Servicio encargado de la facturación.
# En esta práctica, las facturas se almacenan en memoria (no en la base de datos).
class BillingService:
    def __init__(self) -> None:
        # Diccionario de facturas almacenadas: {id: factura}.
        self._invoices: dict[int, Invoice] = {}
        # Contador para generar nuevos IDs de factura.
        self._next_id = 1

    # Crea una factura vacía y la almacena en memoria.
    def create_invoice(self, client_id: int, pet_id: int, appointment_id: int) -> Invoice:
        invoice = Invoice(
            id=self._next_id,
            client_id=client_id,
            pet_id=pet_id,
            appointment_id=appointment_id,
            created_at=datetime.now(),
            status=InvoiceStatus.DRAFT,
        )
        self._invoices[self._next_id] = invoice
        self._next_id += 1
        return invoice

    # Recupera una factura por su ID.
    def get_invoice(self, invoice_id: int) -> Invoice | None:
        return self._invoices.get(invoice_id)

    # Devuelve todas las facturas creadas.
    def list_invoices(self) -> list[Invoice]:
        return list(self._invoices.values())
