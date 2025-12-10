import streamlit as st
from src.db import Database

# ---------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="Usuarios y roles - ClinicVet", page_icon="🔐", layout="wide")
st.title("🔐 Gestión de usuarios y roles")

# Creamos conexión con la BD
db = Database()
db.init_schema()

# ---------------------------------------------------------
# CREAR ADMIN POR DEFECTO SI NO EXISTE NINGÚN USUARIO
# ---------------------------------------------------------
# Esto evita que la app se quede bloqueada sin un primer administrador
if db.query("SELECT COUNT(*) FROM users")[0][0] == 0:
    db.execute(
        "INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')"
    )
    st.warning("Se creó automáticamente un usuario inicial: usuario='admin', contraseña='admin'")

# ---------------------------------------------------------
# INICIALIZAR SESSION_STATE PARA USUARIOS
# ---------------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

st.divider()

# =========================================================
# SELECCIONAR ENTRE LOGIN Y REGISTRO
# =========================================================
# Permite que el usuario elija si quiere iniciar sesión o crear cuenta
mode = st.radio("Selecciona una opción:", ["Iniciar sesión", "Crear cuenta"])

st.divider()

# =========================================================
# FUNCIÓN PARA LOGIN
# =========================================================
def login(username, password):
    """
    Comprueba si existe un usuario con ese nombre y contraseña.
    Devuelve (id, username, role) si existe.
    Devuelve None si no existe.
    """
    result = db.query(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    return result[0] if result else None

# =========================================================
# MODO: INICIAR SESIÓN
# =========================================================
if mode == "Iniciar sesión":

    st.subheader("🔑 Iniciar sesión")

    # Datos del login
    login_user = st.text_input("Usuario")
    login_pass = st.text_input("Contraseña", type="password")

    # Botón para iniciar sesión
    if st.button("Entrar"):
        user = login(login_user, login_pass)

        if user:
            # Guardamos el usuario en la sesión
            st.session_state.user = {
                "id": user[0],
                "username": user[1],
                "role": user[2],
            }
            st.success(f"Bienvenido, {user[1]} (rol: {user[2]})")
            st.rerun()  # Recargar para mostrar opciones del usuario
        else:
            st.error("Usuario o contraseña incorrectos.")

# =========================================================
# MODO: CREAR CUENTA (ACCESIBLE SIN LOGIN)
# =========================================================
if mode == "Crear cuenta":

    st.subheader("👤 Crear cuenta nueva")

    # Inputs del nuevo usuario
    new_user = st.text_input("Nuevo usuario")
    new_pass = st.text_input("Contraseña", type="password")

    new_role = st.selectbox("Rol", ["admin", "vet", "receptionist"])


    # Botón para registrar
    if st.button("Registrar usuario"):
        if not new_user or not new_pass:
            st.error("Debes rellenar usuario y contraseña.")
        else:
            try:
                db.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (new_user, new_pass, new_role),
                )
                st.success(f"Usuario '{new_user}' creado correctamente. Ahora inicia sesión.")
            except Exception:
                # Manejo de usuario duplicado
                st.error("Ese usuario ya existe.")

# =========================================================
# SI EL USUARIO YA HA INICIADO SESIÓN
# =========================================================
if st.session_state.user:

    st.divider()

    # Mostrar datos del usuario logueado
    st.subheader(f"👋 Sesión iniciada como: {st.session_state.user['username']} ({st.session_state.user['role']})")

    # Botón de logout
    if st.button("Cerrar sesión"):
        st.session_state.user = None
        st.rerun()

    # --------------------------------------------------------
    # LISTADO DE USUARIOS (SOLO ADMIN)
    # --------------------------------------------------------
    if st.session_state.user["role"] == "admin":

        st.subheader("📋 Usuarios registrados")

        users = db.query("SELECT id, username, role FROM users")

        if users:
            for uid, uname, urole in users:
                st.write(f"• **{uname}** — Rol: `{urole}` (ID {uid})")
        else:
            st.info("No hay usuarios registrados aún.")
