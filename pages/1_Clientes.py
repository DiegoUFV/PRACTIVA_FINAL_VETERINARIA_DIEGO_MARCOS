import streamlit as st
from src.db import Database
from src.services.client_service import ClientService
from src.utils import validate_email, validate_phone

st.set_page_config(page_title="Clientes - ClinicVet", page_icon="👤", layout="wide")

st.title("👤 Gestión de Clientes")
st.markdown("---")

db = Database()
db.init_schema()
client_service = ClientService(db)

# ======================================================
# TABS — mismo estilo que Mascotas
# ======================================================
tabs = st.tabs([
    "➕ Registrar cliente",
    "📋 Listar clientes",
    "🔍 Buscar cliente",
    "⚙️ Editar / Eliminar"
])

# ======================================================
# TAB 1 — REGISTRAR CLIENTE
# ======================================================
with tabs[0]:
    st.subheader("➕ Registrar nuevo cliente")

    with st.form("form_registrar_cliente"):
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


# ======================================================
# TAB 2 — LISTAR CLIENTES (con tarjetitas)
# ======================================================
with tabs[1]:
    st.subheader("📋 Listado de clientes")

    clients = client_service.list_clients()

    if not clients:
        st.info("No hay clientes registrados todavía.")
    else:
        for c in clients:
            client_id, name, email, phone = c

            st.markdown(
                f"""
                <div style='
                    background-color:#111;
                    padding:15px;
                    border-radius:10px;
                    border:1px solid #444;
                    margin-bottom:12px;
                '>
                    <h4 style='margin:0;color:white;'>{name}</h4>
                    <p style='margin:2px;color:#bbb;'>
                        <b>ID:</b> {client_id}<br>
                        <b>Email:</b> {email if email else "Sin correo"}<br>
                        <b>Teléfono:</b> {phone if phone else "Sin teléfono"}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ======================================================
# TAB 3 — BUSCAR CLIENTE (por nombre)
# ======================================================
with tabs[2]:
    st.subheader("🔍 Buscar cliente")

    name_query = st.text_input("Nombre o parte del nombre")

    if st.button("Buscar"):
        results = client_service.find_by_name(name_query)

        if not results:
            st.warning("No se encontraron clientes con ese nombre.")
        else:
            for c in results:
                st.markdown(
                    f"""
                    <div style='
                        background-color:#111;
                        padding:15px;
                        border-radius:10px;
                        border:1px solid #444;
                        margin-bottom:12px;
                    '>
                        <h4 style='margin:0;color:white;'>{c[1]}</h4>
                        <p style='margin:2px;color:#bbb;'>
                            <b>ID:</b> {c[0]}<br>
                            <b>Email:</b> {c[2] if c[2] else "Sin correo"}<br>
                            <b>Teléfono:</b> {c[3] if c[3] else "Sin teléfono"}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ======================================================
# TAB 4 — EDITAR / ELIMINAR CLIENTE
# ======================================================
with tabs[3]:
    st.subheader("⚙️ Editar o eliminar cliente")

    client_id_edit = st.number_input("ID del cliente", min_value=1, step=1)

    if st.button("Cargar datos"):
        client = client_service.get_client_by_id(client_id_edit)

        if not client:
            st.error("Cliente no encontrado.")
        else:
            st.success("Cliente encontrado")

            name_edit = client[1]
            email_edit = client[2]
            phone_edit = client[3]

            with st.form("form_editar_cliente"):
                new_name = st.text_input("Nombre", value=name_edit)
                new_email = st.text_input("Correo electrónico", value=email_edit)
                new_phone = st.text_input("Teléfono", value=phone_edit)

                guardar = st.form_submit_button("Guardar cambios")
                borrar = st.form_submit_button("Eliminar cliente")

                if guardar:
                    client_service.update_client(client_id_edit, new_name, new_email, new_phone)
                    st.success("Cliente actualizado correctamente.")

                if borrar:
                    client_service.delete_client(client_id_edit)
                    st.warning("Cliente eliminado.")
