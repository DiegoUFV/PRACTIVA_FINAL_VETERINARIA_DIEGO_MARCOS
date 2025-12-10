import streamlit as st

st.set_page_config(page_title="Usuarios y roles - ClinicVet", page_icon="🔐", layout="wide")

st.title("Gestión de usuarios y roles")

st.warning(
    "La gestión real de usuarios (login, permisos, etc.) aún no está implementada. "
    "Esta página solo sirve como placeholder para diseñar la interfaz."
)

st.subheader("Crear usuario (mock)")
username = st.text_input("Nombre de usuario")
password = st.text_input("Contraseña", type="password")
role = st.selectbox("Rol", ["admin", "vet", "receptionist"])

if st.button("Crear usuario (solo demo)"):
    if not username or not password:
        st.error("Usuario y contraseña son obligatorios.")
    else:
        st.success(f"Usuario '{username}' con rol '{role}' creado (demo, no persistente).")
