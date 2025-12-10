import streamlit as st
from src.db import Database
from src.services import ReportingService

st.set_page_config(page_title="Informes y estadísticas - ClinicVet", page_icon="📊", layout="wide")

st.title("Informes y estadísticas")

db = Database()
db.init_schema()
reporting = ReportingService(db)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Clientes", reporting.count_clients())
with col2:
    st.metric("Mascotas", reporting.count_pets())
with col3:
    st.metric("Citas", reporting.count_appointments())

st.info(
    "En el futuro añadiremos informes más detallados, por ejemplo: ingresos mensuales, "
    "número de citas canceladas, especies más comunes, etc."
)
