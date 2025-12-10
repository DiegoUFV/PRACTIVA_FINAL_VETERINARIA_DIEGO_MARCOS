🐾 ClinicVet – Sistema de Gestión para Clínica Veterinaria
Proyecto Final — Programación II (UFV)
📌 Descripción general

ClinicVet es una aplicación completa para la gestión interna de una clínica veterinaria.
El objetivo del proyecto es implementar un sistema realista que permita administrar:

Clientes

Mascotas

Citas veterinarias

Veterinarios

Historial clínico

Facturación

Informes y estadísticas

Usuarios y roles

La aplicación está desarrollada en Python + Streamlit, y utiliza una base de datos SQLite gestionada mediante un sistema de servicios y modelos organizados en la carpeta src/.

Este proyecto demuestra el uso de arquitectura por capas, diseño limpio, separación de responsabilidades (principios SOLID), validaciones, manejo de estado en Streamlit y persistencia de datos.

🎯 Alcance del proyecto

Este trabajo forma parte de la asignatura Programación II, y su finalidad es aplicar todos los conceptos vistos durante el curso:

⭐ Programación estructurada y modular

Código organizado por módulos (models, services, utils, pages)

Reutilización de funciones

Estructuras de datos coherentes

⭐ Arquitectura multicapa

UI (Streamlit)

Servicios (lógica de negocio)

Modelos (representación de entidades)

Base de datos (SQLite)

⭐ Buenas prácticas de programación

Principios SOLID

Single Responsibility en servicios y modelos

Código limpio y documentado

Validaciones robustas (emails, fechas, horarios, teléfonos…)

⭐ Gestión de estado en Streamlit

Utilización de st.session_state para evitar reruns y permitir edición fluida de datos.

⭐ Persistencia con SQLite

Tablas creadas desde Database.init_schema():

clients

pets

appointments

medical_records

invoices

invoice_lines

users

vets

⭐ Pruebas automáticas

Incluye archivos de test en la carpeta tests/, que verifican:

Modelos

Servicios

Validadores

Facturas

Sistema de usuarios

🖥️ Características principales de la aplicación
👤 Gestión de clientes

Registrar cliente

Listar clientes con tarjetas visuales

Buscar por ID o nombre

Editar y eliminar

Ver mascotas asociadas

🐶 Gestión de mascotas

Registrar mascota vinculada a un cliente

Listar mascotas por cliente

Ficha completa

Editar / eliminar

Asociado al historial clínico y citas

📅 Gestión de citas

Registrar cita con validación de horarios:

L–V: 9:00–20:00

Sábado: 10:00–14:00

Domingo: cerrado

Listar citas por día

Buscar cita

Editar cita

Cancelar cita

🩺 Gestión de veterinarios

Registrar veterinario

Listar con tarjetas

Buscar por nombre

Editar / eliminar

Asignación a citas y tratamientos (ampliable)

📘 Historial clínico

Registrar entradas por mascota

Fecha, tipo de registro y descripción

Consultar historial completo

💳 Facturación

Generar facturas

Añadir líneas con conceptos, cantidad y precio

Listar facturas

Gestionar estado (pagada / pendiente)

📈 Informes y estadísticas

Número de citas por día/mes

Veterinarios activos

Mascotas registradas por cliente

Ingresos aproximados (facturación)

🔐 Usuarios y roles

(En desarrollo / opcional)

Roles: admin, veterinario, recepcionista

Autenticación básica

🛠️ Tecnologías utilizadas
Tecnología	Uso
Python 3.x	Lenguaje principal
Streamlit	Interfaz gráfica multipágina
SQLite	Persistencia de datos
Pytest	Pruebas automáticas
Datetime	Manejo de fechas de citas
Hashlib	Seguridad en contraseñas
Decoradores	Validación y control
