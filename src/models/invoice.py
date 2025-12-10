from datetime import datetime
from enum import Enum
from typing import List

# Enumeración con los posibles estados de una factura.
class InvoiceStatus(str, Enum):
    DRAFT = "draft"        # // Borrador: aún editable.
    PAID = "paid"          # // Factura pagada.
    CANCELLED = "cancelled"  # // Factura anulada.

# Clase que representa una línea de factura (un concepto facturable).
class InvoiceLine:
    def __init__(self, description: str, quantity: float, unit_price: float) -> None:
        # Descripción del servicio o producto.
        self.description = description
        # Cantidad (por ejemplo, número de unidades u horas).
        self.quantity = quantity
        # Precio unitario.
        self.unit_price = unit_price

    @property
    def total(self) -> float:
        # Importe total de la línea: cantidad * precio unitario.
        return self.quantity * self.unit_price

# Clase que representa una factura completa.
class Invoice:
    def __init__(
        self,
        id: int,
        client_id: int,
        pet_id: int,
        appointment_id: int,
        created_at: datetime,
        status: InvoiceStatus = InvoiceStatus.DRAFT,
        vat_rate: float = 0.21,
        lines: List[InvoiceLine] | None = None,
    ) -> None:
        # Identificador único de la factura.
        self.id = id
        # Identificador del cliente al que se factura.
        self.client_id = client_id
        # Identificador de la mascota asociada (por contexto de la factura).
        self.pet_id = pet_id
        # Identificador de la cita vinculada a la factura.
        self.appointment_id = appointment_id
        # Fecha y hora de creación de la factura.
        self.created_at = created_at
        # Estado de la factura (borrador, pagada, cancelada).
        self.status = status
        # Tipo de IVA aplicado (por defecto, 21%).
        self.vat_rate = vat_rate
        # Lista de líneas de factura (vacía por defecto).
        self.lines: List[InvoiceLine] = lines if lines is not None else []

    def add_line(self, line: InvoiceLine) -> None:
        # Añade una nueva línea a la factura.
        self.lines.append(line)

    @property
    def subtotal(self) -> float:
        # Suma de los importes de todas las líneas (sin IVA).
        return sum(line.total for line in self.lines)

    @property
    def vat_amount(self) -> float:
        # Importe total de IVA calculado sobre el subtotal.
        return self.subtotal * self.vat_rate

    @property
    def total(self) -> float:
        # Importe total de la factura: subtotal + IVA.
        return self.subtotal + self.vat_amount
