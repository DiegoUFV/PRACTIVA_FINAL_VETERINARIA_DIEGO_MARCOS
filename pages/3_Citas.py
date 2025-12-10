import streamlit as st
from datetime import datetime, date
from src.db import Database
from src.services import AppointmentService, ClientService, PetService
from src.models import AppointmentStatus
from src.utils.time_utils import is_valid_appointment_time

st.set_page_config(page_title="Citas - ClinicVet", page_icon="📅", layout="wide")

st.title("📅 Gestión de Citas")
st.markdown("---")

db = Database()
db.init_schema()

appointment_service = AppointmentService(db)
client_service = ClientService(db)
pet_service = PetService(db)

# ======================================================
# TABS
# ======================================================
tabs = st.tabs([
    "➕ Registrar cita",
    "📋 Listar citas",
    "🔍 Buscar cita",
    "⚙️ Editar / Cancelar"
])


# ======================================================
# TAB 1 — REGISTRAR CITA
# ======================================================
with tabs[0]:
    st.subheader("➕ Registrar nueva cita")

    clients = client_service.list_clients()

    if not clients:
        st.info("Primero debes registrar clientes y mascotas.")
    else:
        client_options = {f"{c[1]} (ID {c[0]})": c[0] for c in clients}
        client_label = st.selectbox("Cliente", list(client_options.keys()))
        client_id = client_options[client_label]

        pets = pet_service.list_pets_by_client(client_id)

        if not pets:
            st.error("Este cliente no tiene mascotas.")
        else:
            pet_options = {f"{p[1]} (ID {p[0]})": p[0] for p in pets}
            pet_label = st.selectbox("Mascota", list(pet_options.keys()))
            pet_id = pet_options[pet_label]

            vet_id = st.number_input("ID veterinario", min_value=1, step=1)

            col1, col2 = st.columns(2)
            with col1:
                day = st.date_input("Fecha", value=date.today())
            with col2:
                time_val = st.time_input("Hora")

            reason = st.text_input("Motivo de la consulta")

            if st.button("Crear cita"):
                scheduled_at = datetime.combine(day, time_val)

                # Validación de horario
                ok, message = is_valid_appointment_time(scheduled_at)
                if not ok:
                    st.error(message)
                else:
                    appointment_service.create_appointment(pet_id, vet_id, scheduled_at, reason)
                    st.success("Cita registrada correctamente.")


# ======================================================
# TAB 2 — LISTAR CITAS
# ======================================================
with tabs[1]:
    st.subheader("📋 Listar citas por día")

    selected_day = st.date_input("Selecciona un día", value=date.today())

    rows = appointment_service.list_appointments_by_date(selected_day.isoformat())

    if not rows:
        st.info("No hay citas para ese día.")
    else:
        for r in rows:
            ap_id, pet_id, vet_id, scheduled_at, reason, status = r
            st.markdown(
                f"""
                <div style='padding: 15px; border-radius: 10px; background-color:#111;
                border: 1px solid #444; margin-bottom:12px;'>
                    <h4 style='color:white;'>Cita #{ap_id}</h4>
                    <p style='color:#bbb;'>
                        <b>Mascota ID:</b> {pet_id}<br>
                        <b>Veterinario ID:</b> {vet_id}<br>
                        <b>Fecha y hora:</b> {scheduled_at}<br>
                        <b>Motivo:</b> {reason}<br>
                        <b>Estado:</b> {status}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ======================================================
# TAB 3 — BUSCAR CITA POR ID
# ======================================================
with tabs[2]:
    st.subheader("🔍 Buscar cita")

    ap_id_search = st.number_input("ID de cita", min_value=1, step=1)

    if st.button("Buscar cita"):
        ap = appointment_service.get_appointment_by_id(ap_id_search)

        if not ap:
            st.error("No existe una cita con ese ID.")
        else:
            ap_id, pet_id, vet_id, scheduled_at, reason, status = ap
            st.success(f"Cita #{ap_id} encontrada")
            st.write(f"**Mascota ID:** {pet_id}")
            st.write(f"**Veterinario ID:** {vet_id}")
            st.write(f"**Fecha y hora:** {scheduled_at}")
            st.write(f"**Motivo:** {reason}")
            st.write(f"**Estado:** {status}")


# ======================================================
# TAB 4 — EDITAR / CANCELAR CITA
# ======================================================
with tabs[3]:
    st.subheader("⚙️ Editar o cancelar cita")

    ap_id_edit = st.number_input("ID de la cita", min_value=1, step=1)

    if st.button("Cargar datos de cita"):
        ap = appointment_service.get_appointment_by_id(ap_id_edit)

        if not ap:
            st.error("Cita no encontrada.")
            st.session_state["appointment_loaded"] = None
        else:
            st.session_state["appointment_loaded"] = ap
            st.success("Cita cargada correctamente.")

    ap_loaded = st.session_state.get("appointment_loaded", None)

    if ap_loaded:
        ap_id, pet_id, vet_id, scheduled_at_str, reason, status = ap_loaded
        scheduled_at_dt = datetime.fromisoformat(scheduled_at_str)

        with st.form("edit_appointment_form"):
            new_reason = st.text_input("Motivo", value=reason)
            new_date = st.date_input("Fecha", value=scheduled_at_dt.date())
            new_time = st.time_input("Hora", value=scheduled_at_dt.time())

            save = st.form_submit_button("Guardar cambios")
            cancel = st.form_submit_button("Cancelar cita")

            if save:
                new_dt = datetime.combine(new_date, new_time)
                ok, message = is_valid_appointment_time(new_dt)

                if not ok:
                    st.error(message)
                else:
                    appointment_service.update_appointment(ap_id, new_dt, new_reason)
                    st.success("Cita actualizada correctamente.")
                    st.session_state["appointment_loaded"] = appointment_service.get_appointment_by_id(ap_id)

            if cancel:
                appointment_service.update_status(ap_id, AppointmentStatus.CANCELLED.value)
                st.warning("Cita cancelada.")
                st.session_state["appointment_loaded"] = appointment_service.get_appointment_by_id(ap_id)
