import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Título y descriçión de la app
st.set_page_config(page_title="Tickets de Soporte", page_icon="🎫")
st.title("Tickets de Soporte 🎫")
st.write(
    """
    Actividades del área de sistemas
    """
)

# Crear un data frame para guardar en el estado de sesión
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "ID", "FECHA", "USUARIO", "EMPRESA", "ASISTENCIA", "ESTADO", "ATENDIÓ", "DESCRIPCION"
    ])

# Arreglo de asistencias
asistencias = [
    "Carpeta Compartida",
    "Celular",
    "Conmutador"
    "Correo"
    "Documento"
    "Escáner",
    "Equipo",
    "SAE",
    "Software",
]

# Arreglo de usuarios
usuarios = [
    "Aaron Othokani",
    "Alma Salaís",
    "Ana Enriquez",
    "Antonio López",
    "Brenda García",
]

#Arreglo de empresas
empresas = [
    "CODEQUIM",
    "MEDICA DEL VALLE",
    "KILLVEC",
    "EXTERPLAG",
    "PAINTSHIELD",
]

# Arreglo del personal
sistemas = [
    "León Hernández",
    "Ismael",
]

# Sección para añadir un Ticket
st.header("Añadir un ticket")

# Añadimos tickets vía `st.form` con algunnos widgets de entrada. Si los widgets se usan
# en un form, la app solo los devolverá cuando se haya pulsado el botón de terminar
with st.form("add_ticket_form"):
    usuario = st.selectbox("Usuario", usuarios)
    empresa = st.selectbox("Empresa", empresas)
    asistencia = st.selectbox("Asistencia", asistencias)
    atencion = st.selectbox("Atendió", sistemas)
    descripcion = st.text_area("Descripción")
    terminar = st.form_submit_button("Terminar")

if terminar:
    # Creamos un data frame para el nuevo ticket y lo unimos al datframe de tickets existentes
    if st.session_state.df.empty:
        no_ticket = 0000
    else:
        no_ticket = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{no_ticket+1}",
                "FECHA": today,
                "USUARIO": usuario,
                "EMPRESA": empresa,
                "ASISTENCIA": asistencia,
                "ESTADO": "Abierto",
                "ATENDIÓ": atencion,
                "DESCRICPION": descripcion,
                              
            }
        ]
    )

    # Mensaje de creación de ticket
    st.write("¡Ticket registrado! Aquí los detalles de tu ticket:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

# Sección para ver y editar los tickets existentes
st.header("Tickets existentes")
st.write(f"Número de tickets: `{len(st.session_state.df)}`")

st.info(
    "Puedes editar un ticket haciendo click en la celda. Los gráficos de abajo se actualizarán automáticamente."
    "También puedes ordenar las columnas haciendo click en las cabeceras de las columnas",
    icon="✍️",
)

# Mostrar el data frame de tickets editable
# Los datos editados se devuelven como un nuevo data frame
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),
        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,
        ),
    },
    # Bloqueamos la edición del ID y de la fecha del ticket
    disabled=["ID", "FECHA"],
)

# Sección para mostrar las métricas del área
st.header("Métricas")

col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.ESTADO == "Solucionado"])
col1.metric(label="Total de Tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Tiempo promedio de respuesta (hrs)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("Estatus de Ticket mensual")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(FECHA):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")
