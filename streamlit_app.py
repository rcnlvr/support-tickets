import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Tickets de Soporte", page_icon="🎫")
st.title("Tickets de Soporte 🎫")
st.write(
    """
    Actividades del área de sistemas
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

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

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "FECHA": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
        "USUARIO": np.random.choice(usuarios, size=100),
        "ASISTENCIA": np.random.choice(asistencias, size=100),
        "ESTADO": np.random.choice(["Solucionado", "En proceso"], size=100),
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df


# Sección para añadir un Ticket
st.header("Añadir un ticket")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):
    asistencia = st.text_area("Descripción")
    usuario = st.selectbox("Priority", ["High", "Medium", "Low"])
    terminar = st.form_submit_button("Terminar")

if terminar:
    # Make a dataframe for the new ticket and append it to the dataframe in session
    # state.
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "FECHA": today,
                "USUARIO": usuario, 
                "ASISTENCIA": asistencia,
                "ESTADO": "Abierto",
                              
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

# Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
# cells. The edited data is returned as a new dataframe.
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

# Show metrics side by side using `st.columns` and `st.metric`.
col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.ESTADO == "Solucionado"])
col1.metric(label="Total de Tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# Show two Altair charts using `st.altair_chart`.
st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
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
