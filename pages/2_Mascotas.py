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
# TABS (sin listado) — en el orden que tú quieres
# ======================================================
tabs = st.tabs(["➕ Registrar mascota", "📝 Ficha completa", "⚙️ Editar / Eliminar"])

# ======================================================
# TAB 1 — REGISTRAR MASCOTA (lo primero que querías)
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
# TAB 2 — FICHA COMPLETA (buscar por ID)
# ======================================================
with tabs[1]:
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
# TAB 3 — EDITAR O ELIMINAR
# ======================================================
with tabs[2]:
    st.subheader("⚙️ Editar o eliminar mascota")

    pet_id_edit = st.number_input("ID de la mascota", min_value=1, step=1, key="edit_pet")

    if st.button("Cargar datos"):
        pet = pet_service.get_pet_by_id(pet_id_edit)

        if not pet:
            st.error("Mascota no encontrada.")
        else:
            name_edit = st.text_input("Nombre", value=pet[2])
            species_edit = st.text_input("Especie", value=pet[3])
            breed_edit = st.text_input("Raza", value=pet[4])
            sex_edit = st.selectbox("Sexo", ["Macho", "Hembra"], index=0 if pet[5] == "Macho" else 1)

            if st.button("Guardar cambios"):
                pet_service.update_pet(
                    pet_id_edit,
                    name_edit,
                    species_edit,
                    breed_edit,
                    sex_edit
                )
                st.success("Mascota actualizada.")

            if st.button("Eliminar mascota"):
                pet_service.delete_pet(pet_id_edit)
                st.warning("Mascota eliminada.")