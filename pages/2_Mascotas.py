import streamlit as st
from src.db import Database
from src.services import ClientService, PetService

st.set_page_config(page_title="Mascotas - ClinicVet", page_icon="🐶", layout="wide")

st.title("Gestión de mascotas")

db = Database()
db.init_schema()
client_service = ClientService(db)
pet_service = PetService(db)

clients = client_service.list_clients()
client_options = {f"{c[1]} (ID {c[0]})": c[0] for c in clients}

st.subheader("Registro de mascota")
if not clients:
    st.info("Primero debes registrar algún cliente.")
else:
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

st.subheader("Listado de mascotas por cliente")
if clients:
    owner_filter_label = st.selectbox("Selecciona cliente", list(client_options.keys()), key="owner_filter")
    owner_id = client_options[owner_filter_label]
    pets = pet_service.list_pets_by_client(owner_id)
    if pets:
        st.table(
            {
                "ID": [p[0] for p in pets],
                "Nombre": [p[1] for p in pets],
                "Especie": [p[2] for p in pets],
                "Raza": [p[3] for p in pets],
                "Sexo": [p[4] for p in pets],
            }
        )
    else:
        st.info("Este cliente no tiene mascotas registradas.")
