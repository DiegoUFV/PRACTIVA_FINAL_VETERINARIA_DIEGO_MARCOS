import streamlit as st
import pandas as pd
import altair as alt

from src.db import Database
from src.services import ReportingService

# Configuración general de la página
st.set_page_config(
    page_title="Informes y estadísticas - ClinicVet",
    page_icon="📊",
    layout="wide",
)

# Título principal
st.title("📊 Informes y estadísticas")

# Inicialización de base de datos y servicio de reportes
db = Database()
db.init_schema()
reporting = ReportingService(db)

# -----------------------------
# MÉTRICAS PRINCIPALES
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    # Mostrar número total de clientes
    st.metric("Clientes", reporting.count_clients())

with col2:
    # Mostrar número total de mascotas
    st.metric("Mascotas", reporting.count_pets())

with col3:
    # Mostrar número total de citas
    st.metric("Citas", reporting.count_appointments())

st.divider()

# -----------------------------
# GRÁFICO 1: Pie chart de mascotas por especie
# -----------------------------
st.subheader("🐾 Distribución de mascotas por especie (Pie chart)")

species_data = db.query(
    """
    SELECT species, COUNT(*)
    FROM pets
    GROUP BY species
    """
)

df_species = pd.DataFrame(species_data, columns=["Especie", "Cantidad"])

if len(df_species) > 0:
    # Gráfico circular con Altair
    pie_chart = alt.Chart(df_species).mark_arc().encode(
        theta="Cantidad:Q",
        color="Especie:N",
        tooltip=["Especie:N", "Cantidad:Q"],
    )
    st.altair_chart(pie_chart, use_container_width=True)
else:
    st.info("Aún no hay mascotas registradas para generar este gráfico.")

st.divider()

# -----------------------------
# GRÁFICO 2: Donut chart de citas por estado
# -----------------------------
st.subheader("📅 Citas por estado (Donut chart)")

appointments_data = db.query(
    """
    SELECT status, COUNT(*)
    FROM appointments
    GROUP BY status
    """
)

df_status = pd.DataFrame(appointments_data, columns=["Estado", "Cantidad"])

if len(df_status) > 0:
    # Gráfico donut con Altair
    donut_chart = alt.Chart(df_status).mark_arc(innerRadius=50).encode(
        theta="Cantidad:Q",
        color="Estado:N",
        tooltip=["Estado:N", "Cantidad:Q"],
    )
    st.altair_chart(donut_chart, use_container_width=True)
else:
    st.info("No hay citas registradas para mostrar el gráfico por estado.")

st.divider()

# -----------------------------
# GRÁFICO SIMPLE: Citas por día (Line chart)
# -----------------------------
st.subheader("📈 Citas por día (Gráfico sencillo)")

citas_por_dia = db.query(
    """
    SELECT DATE(scheduled_at), COUNT(*)
    FROM appointments
    GROUP BY DATE(scheduled_at)
    ORDER BY DATE(scheduled_at)
    """
)

df_citas_dia = pd.DataFrame(citas_por_dia, columns=["Fecha", "Citas"])

# Convertimos Fecha a string para evitar problemas con horas
df_citas_dia["Fecha"] = df_citas_dia["Fecha"].astype(str)

if len(df_citas_dia) > 0:
    st.line_chart(df_citas_dia, x="Fecha", y="Citas")
else:
    st.info("Todavía no hay citas registradas para mostrar el gráfico diario.")
