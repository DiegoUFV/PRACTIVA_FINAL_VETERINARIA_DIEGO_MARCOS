import streamlit as st
from src.services import BillingService

st.set_page_config(page_title="Facturación - ClinicVet", page_icon="💶", layout="wide")

st.title("Gestión de facturación")

billing_service = BillingService()

st.info(
    "Por ahora la facturación funciona solo en memoria (no se guarda en la base de datos). "
    "Esto se sustituirá por una implementación persistente más adelante."
)

client_id = st.number_input("ID cliente", min_value=1, step=1)
pet_id = st.number_input("ID mascota", min_value=1, step=1)
appointment_id = st.number_input("ID cita", min_value=1, step=1)

if st.button("Crear factura"):
    invoice = billing_service.create_invoice(
        client_id=int(client_id),
        pet_id=int(pet_id),
        appointment_id=int(appointment_id),
    )
    st.success(f"Factura creada con ID {invoice.id}")

st.write("Una vez creada, en futuras iteraciones podremos añadir líneas, aplicar IVA y exportar a PDF.")
