import streamlit as st
import pandas as pd
from datetime import datetime

from src.db import Database

st.set_page_config(page_title="Historia clínica - ClinicVet", page_icon="📋", layout="wide")

# Título de la página
st.title("📋 Historia clínica")

# Conexión a la base de datos
db = Database()
db.init_schema()

st.write("Aquí puedes registrar consultas, tratamientos o vacunas de cada mascota de forma sencilla.")

st.divider()

# -------------------------
# Seleccionar mascota desde la BD
# -------------------------
pets = db.query("SELECT id, name FROM pets ORDER BY name ASC")

if not pets:
    st.warning("No hay mascotas registradas en la base de datos.")
    st.stop()

# Creamos un diccionario nombre -> id
pet_map = {name: pet_id for pet_id, name in pets}

pet_name = st.selectbox("Selecciona una mascota:", list(pet_map.keys()))
pet_id = pet_map[pet_name]

st.success(f"Mascota seleccionada: {pet_name}")

st.divider()

# -------------------------
# Añadir un nuevo registro clínico
# -------------------------
st.subheader("➕ Añadir registro clínico")

record_type = st.selectbox("Tipo de registro:", ["Consulta", "Tratamiento", "Vacuna"])
description = st.text_area("Descripción de la consulta / tratamiento / vacuna:")

if st.button("Guardar registro"):
    if description.strip() == "":
        st.error("La descripción no puede estar vacía.")
    else:
        # Insertamos directamente en la tabla medical_records
        db.execute(
            """
            INSERT INTO medical_records (pet_id, record_date, record_type, description)
            VALUES (?, ?, ?, ?)
            """,
            (pet_id, datetime.now().isoformat(), record_type, description),
        )
        st.success("Registro clínico añadido correctamente.")

st.divider()

# -------------------------
# Mostrar historial clínico desde la BD
# -------------------------
st.subheader("📄 Historial clínico")

rows = db.query(
    """
    SELECT record_date, record_type, description
    FROM medical_records
    WHERE pet_id = ?
    ORDER BY record_date DESC
    """,
    (pet_id,),
)

if rows:
    # Convertimos las filas en un DataFrame
    df = pd.DataFrame(rows, columns=["Fecha", "Tipo", "Descripción"])

    # Opcional: mostrar solo la fecha sin la hora
    df["Fecha"] = df["Fecha"].str.slice(0, 10)

    st.dataframe(df, use_container_width=True)
else:
    st.info("Esta mascota todavía no tiene historial clínico registrado.")