import streamlit as st

st.set_page_config(page_title="ClinicVet", page_icon="🐾", layout="wide")

st.title("ClinicVet - Veterinary Management System")
st.write(
    "Use the sidebar to navigate between sections: clients, pets, appointments, "
    "medical records, billing, vets, reports and user management."
)

st.info(
    "This is an initial project skeleton. Most features are just placeholders "
    "and will be implemented in later iterations."
)
