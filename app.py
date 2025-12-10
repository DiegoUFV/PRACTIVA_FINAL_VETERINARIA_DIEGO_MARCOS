import streamlit as st
import pandas as pd

# Configuración general de la página
st.set_page_config(
    page_title="ClinicVet",
    page_icon="🐾",
    layout="wide"
)

# -----------------------------
# BANNER SUPERIOR (Streamlit puro)
# -----------------------------
st.title("🐾 Bienvenido a ClinicVet")
st.markdown("### Tu clínica veterinaria de confianza.")

st.divider()

# -----------------------------
# SECCIÓN DE INFORMACIÓN GENERAL
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.header("📍 Información de contacto")

    st.subheader("Dirección")
    st.write("Puerta del Sol, Madrid, España")

    st.subheader("Teléfono")
    st.write("📞 91 123 45 67")

    st.subheader("Correo electrónico")
    st.write("📧 help@clinicavet.com")

    st.subheader("Horario")
    st.write("""
    - **Lunes a Viernes:** 9:00 - 20:00  
    - **Sábados:** 10:00 - 14:00  
    - **Domingos:** Cerrado  
    """)

with col2:
    st.header("📌 Mapa interactivo")
    
    # Coordenadas del centro (Madrid)
    map_data = pd.DataFrame({
        "lat": [40.4168],
        "lon": [-3.7038],
    })

    st.map(map_data, zoom=12)

# -----------------------------
# SECCIÓN SOBRE NOSOTROS
# -----------------------------
st.divider()
st.header("🐶 Sobre nosotros")

st.write("""
Somos una clínica veterinaria con más de **10 años de experiencia**,  
especializada en el cuidado integral de perros, gatos y animales exóticos.

Nuestro equipo trabaja para ofrecer:

- Atención personalizada  
- Diagnósticos rápidos y precisos  
- Servicios integrales de salud animal  
""")

# -----------------------------
# SERVICIOS PRINCIPALES
# -----------------------------
st.divider()
st.header("✨ Nuestros servicios")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🩺 Consultas generales")
    st.write("Revisiones, diagnósticos y atención profesional.")

with c2:
    st.subheader("💉 Vacunación y prevención")
    st.write("Programas completos de vacunación para tu mascota.")

with c3:
    st.subheader("🧪 Análisis clínicos")
    st.write("Laboratorio propio para resultados rápidos.")

c4, c5, c6 = st.columns(3)

with c4:
    st.subheader("🐾 Cirugía menor")
    st.write("Intervenciones seguras y seguimiento postoperatorio.")

with c5:
    st.subheader("✂️ Peluquería canina")
    st.write("Cuidado estético especializado.")

with c6:
    st.subheader("🚑 Urgencias")
    st.write("Atención inmediata para emergencias las 24h.")

