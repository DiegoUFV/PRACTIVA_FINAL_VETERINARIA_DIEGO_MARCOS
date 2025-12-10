import streamlit as st
from datetime import datetime
from src.db import Database

# ----------------------------------------------------
# CONFIGURACIÓN INICIAL DE STREAMLIT
# ----------------------------------------------------
st.set_page_config(page_title="Facturación - ClinicVet", page_icon="💶", layout="wide")
st.title("💶 Gestión de facturación")

# ----------------------------------------------------
# CONEXIÓN A LA BASE DE DATOS
# ----------------------------------------------------
# Creamos un objeto Database que conecta a SQLite
db = Database()
db.init_schema()   # Asegura que todas las tablas existan

st.info("La facturación está completamente integrada con la base de datos SQLite.")

st.divider()


# ====================================================
# 1) CREAR UNA FACTURA (TABLA invoices)
# ====================================================
st.subheader("➕ Crear nueva factura")

# Inputs básicos necesarios para una factura
client_id = st.number_input("ID cliente", min_value=1)
pet_id = st.number_input("ID mascota", min_value=1)
appointment_id = st.number_input("ID cita", min_value=1)

# Botón que registra la factura en la BD
if st.button("Crear factura"):
    # Insertamos una nueva factura con estado "draft" (borrador)
    db.execute(
        """
        INSERT INTO invoices (client_id, pet_id, appointment_id, created_at, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (client_id, pet_id, appointment_id, datetime.now().isoformat(), "draft"),
    )

    # Recuperamos el ID autoincremental recién generado
    invoice_id = db.query("SELECT last_insert_rowid()")[0][0]

    st.success(f"Factura creada con ID {invoice_id}")

st.divider()


# ====================================================
# 2) AÑADIR UNA LÍNEA A UNA FACTURA (TABLA invoice_lines)
# ====================================================
st.subheader("🧾 Añadir línea a factura existente")

# Identificamos la factura destino
invoice_id_line = st.number_input("ID factura", min_value=1)

# Datos de la línea de factura
description = st.text_input("Descripción")
quantity = st.number_input("Cantidad", min_value=1.0)      # cantidad de unidades
unit_price = st.number_input("Precio unitario (€)", min_value=0.0)

# Inserta una línea asociada a una factura concreta
if st.button("Añadir línea"):
    db.execute(
        """
        INSERT INTO invoice_lines (invoice_id, description, quantity, unit_price)
        VALUES (?, ?, ?, ?)
        """,
        (invoice_id_line, description, quantity, unit_price),
    )
    st.success("Línea añadida correctamente.")

st.divider()


# ====================================================
# 3) CAMBIAR EL ESTADO DE UNA FACTURA
# ====================================================
st.subheader("🔄 Cambiar estado de factura")

# Seleccionamos factura y estado
invoice_id_status = st.number_input("ID factura a actualizar", min_value=1, key="status_id")
new_status = st.selectbox("Nuevo estado", ["draft", "paid", "cancelled"])

# Actualizamos el estado en la tabla invoices
if st.button("Actualizar estado"):
    db.execute(
        "UPDATE invoices SET status = ? WHERE id = ?",
        (new_status, invoice_id_status),
    )
    st.success("Estado actualizado correctamente.")

st.divider()


# ====================================================
# 4) LISTAR TODAS LAS FACTURAS REGISTRADAS
# ====================================================
st.subheader("📋 Facturas registradas")

# Obtenemos toda la información de la tabla invoices
invoices = db.query(
    """
    SELECT id, client_id, pet_id, appointment_id, created_at, status
    FROM invoices
    ORDER BY created_at DESC
    """
)

# Si la BD contiene facturas, las mostramos
if invoices:

    # Recorremos todas las facturas obtenidas
    for inv_id, client, pet, app, created, status in invoices:

        st.write(f"### 💳 Factura ID {inv_id}")
        st.write(f"- Cliente: {client}")
        st.write(f"- Mascota: {pet}")
        st.write(f"- Cita: {app}")
        st.write(f"- Fecha de creación: {created}")
        st.write(f"- Estado actual: **{status}**")

        # ----------------------------------------------------
        # OBTENER LÍNEAS DE FACTURA RELACIONADAS
        # ----------------------------------------------------
        lines = db.query(
            """
            SELECT description, quantity, unit_price
            FROM invoice_lines
            WHERE invoice_id = ?
            """,
            (inv_id,),
        )

        # Mostramos las líneas si existen
        if lines:
            st.write("#### Líneas de factura:")
            subtotal = 0

            for desc, qty, price in lines:
                total_line = qty * price  # total por línea
                subtotal += total_line     # acumulamos el subtotal

                st.write(f"- {desc}: {qty} × {price}€ = {total_line:.2f}€")

        else:
            st.write("_No hay líneas añadidas en esta factura._")
            subtotal = 0

        # ----------------------------------------------------
        # CÁLCULO DE TOTALES
        # ----------------------------------------------------
        iva = subtotal * 0.21   # IVA al 21%
        total = subtotal + iva  # total final

        st.write(f"**Subtotal:** {subtotal:.2f}€")
        st.write(f"**IVA (21%):** {iva:.2f}€")
        st.write(f"**TOTAL:** {total:.2f}€")

        st.write("---")  # Separador visual entre facturas

else:
    st.info("Todavía no hay facturas registradas en la base de datos.")
