import streamlit as st
from datetime import datetime, date
from src.db import Database
from src.services import AppointmentService, ClientService, PetService
from src.models import AppointmentStatus

st.set_page_config(page_title="Citas - ClinicVet", page_icon="📅", layout="wide")

st.title("Gestión de citas")

db = Database()
db.init_schema()
appointment_service = AppointmentService(db)
client_service = ClientService(db)
pet_service = PetService(db)

clients = client_service.list_clients()
client_options = {f"{c[1]} (ID {c[0]})": c[0] for c in clients}

st.subheader("Registrar nueva cita")
if not clients:
    st.info("Primero debes registrar clientes y mascotas.")
else:
    client_label = st.selectbox("Cliente", list(client_options.keys()))
    client_id = client_options[client_label]
    pets = pet_service.list_pets_by_client(client_id)
    pet_options = {f"{p[1]} (ID {p[0]})": p[0] for p in pets}

    if not pets:
        st.warning("Este cliente no tiene mascotas.")
    else:
        pet_label = st.selectbox("Mascota", list(pet_options.keys()))
        pet_id = pet_options[pet_label]
        vet_id = st.number_input("ID veterinario (placeholder)", min_value=1, step=1)
        col1, col2 = st.columns(2)
        with col1:
            day = st.date_input("Fecha", value=date.today())
        with col2:
            time_str = st.time_input("Hora")
        reason = st.text_input("Motivo de la consulta")

        if st.button("Crear cita"):
            scheduled_at = datetime.combine(day, time_str)
            appointment_service.create_appointment(pet_id, vet_id, scheduled_at, reason)
            st.success("Cita registrada correctamente.")

st.subheader("Citas del día")
selected_day = st.date_input("Selecciona un día para ver las citas", value=date.today(), key="list_day")
rows = appointment_service.list_appointments_by_date(selected_day.isoformat())

if rows:
    st.table(
        {
            "ID": [r[0] for r in rows],
            "Mascota ID": [r[1] for r in rows],
            "Vet ID": [r[2] for r in rows],
            "Fecha y hora": [r[3] for r in rows],
            "Motivo": [r[4] for r in rows],
            "Estado": [r[5] for r in rows],
        }
    )
else:
    st.info("No hay citas para ese día (o aún no se han cargado).")
