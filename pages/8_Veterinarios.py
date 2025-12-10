import streamlit as st
from src.db import Database
from src.services.vet_service import VetService

st.set_page_config(page_title="Veterinarios - ClinicVet", page_icon="🩺", layout="wide")

st.title("🩺 Gestión de Veterinarios")
st.markdown("---")

db = Database()
db.init_schema()

vet_service = VetService(db)

# ======================================================
# TABS
# ======================================================
tabs = st.tabs([
    " Registrar veterinario",
    "📋 Listar veterinarios",
    "🔍 Buscar veterinario",
    "⚙ Editar / Eliminar"
])


# ======================================================
# TAB 1 — REGISTRAR
# ======================================================
with tabs[0]:
    st.subheader(" Registrar nuevo veterinario")

    with st.form("form_registrar_vet"):
        name = st.text_input("Nombre completo")
        speciality = st.text_input("Especialidad")
        schedule = st.text_input("Horario laboral (ej: L-V 9:00-20:00)")
        email = st.text_input("Correo electrónico")
        phone = st.text_input("Teléfono")

        submitted = st.form_submit_button("Registrar")

        if submitted:
            if not name:
                st.error("El nombre es obligatorio.")
            else:
                vet_service.create_vet(name, speciality, schedule, email, phone)
                st.success("Veterinario registrado correctamente.")


# ======================================================
# TAB 2 — LISTAR
# ======================================================
with tabs[1]:
    st.subheader("📋 Veterinarios activos")

    vets = vet_service.list_vets()

    if not vets:
        st.info("No hay veterinarios registrados.")
    else:
        for v in vets:
            vet_id, name, speciality, schedule, email, phone = v

            st.markdown(
                f"""
                <div style='padding:15px; border-radius:10px;
                background-color:#111; border:1px solid #444; margin-bottom:12px;'>
                    <h4 style='color:white; margin:0;'>{name}</h4>
                    <p style='color:#bbb; margin:4px 0;'>
                        <b>ID:</b> {vet_id}<br>
                        <b>Especialidad:</b> {speciality}<br>
                        <b>Horario:</b> {schedule}<br>
                        <b>Email:</b> {email}<br>
                        <b>Teléfono:</b> {phone}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ======================================================
# TAB 3 — BUSCAR
# ======================================================
with tabs[2]:
    st.subheader("🔍 Buscar veterinario")

    search = st.text_input("Nombre del veterinario")

    if st.button("Buscar"):
        results = vet_service.search_vets_by_name(search)

        if not results:
            st.warning("No se encontraron veterinarios.")
        else:
            for v in results:
                vet_id, name, speciality, schedule, email, phone = v

                st.markdown(
                    f"""
                    <div style='padding:15px; border-radius:10px;
                    background-color:#111; border:1px solid #444; margin-bottom:12px;'>
                        <h4 style='color:white; margin:0;'>{name}</h4>
                        <p style='color:#bbb; margin:4px 0;'>
                            <b>ID:</b> {vet_id}<br>
                            <b>Especialidad:</b> {speciality}<br>
                            <b>Horario:</b> {schedule}<br>
                            <b>Email:</b> {email}<br>
                            <b>Teléfono:</b> {phone}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ======================================================
# TAB 4 — EDITAR / ELIMINAR
# ======================================================
with tabs[3]:
    st.subheader("⚙ Editar o eliminar veterinario")

    vet_id_edit = st.number_input("ID del veterinario", min_value=1, step=1)

    if st.button("Cargar datos"):
        vet = vet_service.get_vet_by_id(vet_id_edit)
        if not vet:
            st.error("Veterinario no encontrado.")
            st.session_state["vet_loaded"] = None
        else:
            st.success("Veterinario cargado")
            st.session_state["vet_loaded"] = vet

    vet_loaded = st.session_state.get("vet_loaded", None)

    if vet_loaded:
        vet_id, name, speciality, schedule, email, phone = vet_loaded

        with st.form("form_edit_vet"):
            new_name = st.text_input("Nombre", value=name)
            new_speciality = st.text_input("Especialidad", value=speciality)
            new_schedule = st.text_input("Horario", value=schedule)
            new_email = st.text_input("Correo", value=email)
            new_phone = st.text_input("Teléfono", value=phone)

            save = st.form_submit_button("Guardar cambios")
            delete = st.form_submit_button("Eliminar")

            if save:
                vet_service.update_vet(vet_id, new_name, new_speciality, new_schedule, new_email, new_phone)
                st.success("Veterinario actualizado.")
                st.session_state["vet_loaded"] = vet_service.get_vet_by_id(vet_id)

            if delete:
                vet_service.delete_vet(vet_id)
                st.warning("Veterinario eliminado.")
                st.session_state["vet_loaded"] = None