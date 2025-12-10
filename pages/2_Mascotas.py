import streamlit as st
from src.db import Database
from src.services.client_service import ClientService
from src.services.pet_service import PetService

st.set_page_config(page_title="Mascotas - ClinicVet", page_icon="🐾", layout="wide")

st.title("🐾 Gestión de Mascotas")
st.markdown("---")

db = Database()
db.init_schema()

client_service = ClientService(db)
pet_service = PetService(db)

# ======================================================
# TABS 
# ======================================================
tabs = st.tabs([
    "➕ Registrar mascota",
    "📋 Listado por cliente",
    "📝 Ficha completa",
    "⚙️ Editar / Eliminar"
])


# ======================================================
# TAB 1 — REGISTRAR MASCOTA 
# ======================================================
with tabs[0]:
    st.subheader("➕ Registrar nueva mascota")

    clients = client_service.list_clients()
    if not clients:
        st.info("Primero debes registrar algún cliente.")
    else:
        client_options = {f"{c[1]} (ID {c[0]})": c[0] for c in clients}

        owner_label = st.selectbox("Propietario", list(client_options.keys()))
        name = st.text_input("Nombre de la mascota")
        species = st.text_input("Especie (perro, gato, etc.)")
        breed = st.text_input("Raza (opcional)")
        sex = st.selectbox("Sexo", ["", "Macho", "Hembra"])

        if st.button("Crear mascota"):
            owner_id = client_options[owner_label]
            if not name or not species:
                st.error("Nombre y especie son obligatorios.")
            else:
                pet_service.create_pet(owner_id, name, species, breed or None, sex or None)
                st.success("Mascota registrada correctamente.")

# ======================================================
# ⭐ TAB 2 — LISTADO DE MASCOTAS POR CLIENTE (AÑADIDO)
# ======================================================
with tabs[1]:
    st.subheader("📋 Listado de mascotas por cliente")

    search_mode = st.radio("Buscar cliente por:", ["ID", "Nombre"], horizontal=True)

    client = None

    # Buscar por ID
    if search_mode == "ID":
        client_id_search = st.number_input("ID del cliente", min_value=1, step=1)
        if st.button("Buscar por ID", key="buscar_por_id_mascotas"):
            client = client_service.get_client_by_id(client_id_search)
            if not client:
                st.error("No existe un cliente con ese ID.")

    # Buscar por nombre
    else:
        name_query = st.text_input("Nombre del cliente")
        if st.button("Buscar por nombre", key="buscar_por_nombre_mascotas"):
            results = client_service.find_by_name(name_query)

            if not results:
                st.warning("No se encontró ningún cliente con ese nombre.")
            elif len(results) == 1:
                client = results[0]
            else:
                st.info("Se encontraron varios clientes, selecciona uno:")
                client = st.selectbox(
                    "Seleccionar cliente",
                    results,
                    format_func=lambda c: f"{c[1]} (ID {c[0]})",
                    key="selector_clientes_mascotas"
                )

    # Mostrar mascotas del cliente
    if client:
        st.success(f"Cliente encontrado: {client[1]} (ID {client[0]})")

        pets = pet_service.list_pets_by_client(client[0])

        if not pets:
            st.info("Este cliente no tiene mascotas registradas.")
        else:
            st.subheader("Mascotas del cliente:")

            for p in pets:
                pet_id, name, species, breed, sex = p

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
                            <b>ID:</b> {pet_id}<br>
                            <b>Especie:</b> {species}<br>
                            <b>Raza:</b> {breed if breed else "No especificada"}<br>
                            <b>Sexo:</b> {sex if sex else "No especificado"}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ======================================================
# TAB 2 — FICHA COMPLETA (buscar por ID)
# ======================================================
with tabs[2]:
    st.subheader("📝 Ficha completa de mascota")

    pet_id = st.number_input("ID de mascota", min_value=1, step=1)

    if st.button("Buscar ficha"):
        pet = pet_service.get_pet_by_id(pet_id) if hasattr(pet_service, "get_pet_by_id") else None

        if not pet:
            st.error("No existe una mascota con ese ID.")
        else:
            st.success("Mascota encontrada")
            st.write(f"**ID:** {pet[0]}")
            st.write(f"**Propietario (ID):** {pet[1]}")
            st.write(f"**Nombre:** {pet[2]}")
            st.write(f"**Especie:** {pet[3]}")
            st.write(f"**Raza:** {pet[4]}")
            st.write(f"**Sexo:** {pet[5]}")



# ======================================================
# TAB 4 — EDITAR O ELIMINAR
# ======================================================
with tabs[3]:
    st.subheader("⚙️ Editar o eliminar mascota")

    # Entrada de ID
    pet_id_edit = st.number_input("ID de la mascota", min_value=1, step=1, key="edit_pet_id")

    # Botón para cargar datos
    if st.button("Cargar datos", key="cargar_mascota_btn"):
        pet = pet_service.get_pet_by_id(pet_id_edit)

        if not pet:
            st.error("Mascota no encontrada.")
            st.session_state["pet_loaded"] = None
        else:
            st.success("Mascota cargada")
            st.session_state["pet_loaded"] = pet   # ✔ Guardamos en sesión

    # Recuperar mascota cargada
    pet_loaded = st.session_state.get("pet_loaded", None)

    # Si hay mascota cargada → mostrar formulario
    if pet_loaded:
        pet_id, owner_id, name, species, breed, sex = pet_loaded

        with st.form("editar_mascota_form"):
            name_edit = st.text_input("Nombre", value=name)
            species_edit = st.text_input("Especie", value=species)
            breed_edit = st.text_input("Raza", value=breed)
            sex_edit = st.selectbox(
                "Sexo",
                ["Macho", "Hembra"],
                index=0 if sex == "Macho" else 1
            )

            guardar = st.form_submit_button("Guardar cambios")
            borrar = st.form_submit_button("Eliminar mascota")

            # GUARDAR CAMBIOS
            if guardar:
                pet_service.update_pet(
                    pet_id,
                    name_edit,
                    species_edit,
                    breed_edit,
                    sex_edit
                )
                st.success("Mascota actualizada correctamente.")

                # Recargar datos actualizados
                st.session_state["pet_loaded"] = pet_service.get_pet_by_id(pet_id)

            # ELIMINAR
            if borrar:
                pet_service.delete_pet(pet_id)
                st.warning("Mascota eliminada.")
                
                # Borramos datos cargados
                st.session_state["pet_loaded"] = None
