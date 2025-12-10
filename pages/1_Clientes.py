import streamlit as st
from src.db import Database
from src.services import ClientService
from src.utils import validate_email, validate_phone

st.set_page_config(page_title="Clientes - ClinicVet", page_icon="👤", layout="wide")

st.title("Gestión de clientes")

db = Database()
db.init_schema()
client_service = ClientService(db)

with st.form("nuevo_cliente"):
    st.subheader("Alta de cliente")
    full_name = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    phone = st.text_input("Teléfono")
    submitted = st.form_submit_button("Crear cliente")

    if submitted:
        if not full_name:
            st.error("El nombre es obligatorio.")
        elif email and not validate_email(email):
            st.error("El email no es válido.")
        elif phone and not validate_phone(phone):
            st.error("El teléfono no es válido.")
        else:
            client_service.create_client(full_name, email, phone)
            st.success("Cliente creado correctamente.")

st.subheader("Listado de clientes")
clients = client_service.list_clients()
if clients:
    st.table(
        {
            "ID": [c[0] for c in clients],
            "Nombre": [c[1] for c in clients],
            "Email": [c[2] for c in clients],
            "Teléfono": [c[3] for c in clients],
        }
    )
else:
    st.info("No hay clientes registrados todavía.")
