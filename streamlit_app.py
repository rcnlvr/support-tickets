import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import pytz

# Título y descriçión de la app
st.set_page_config(page_title="Tickets de Soporte", page_icon="🎫")
st.title("Tickets de Soporte 🎫")
st.write(
    """
    Actividades del área de sistemas
    """
)

# Leer el archivo CSV existente
try:
    df = pd.read_csv('tickets.csv')
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "ID", "FECHA", "USUARIO", "EMPRESA", "ASISTENCIA", "HORA INICIO", "HORA FIN", "SOLICITUD", "STATUS", "ATENDIÓ", "DESCRIPCIÓN"
    ])

# Guardar el DataFrame en el estado de sesión
if "df" not in st.session_state:
    st.session_state.df = df

# Arreglo de asistencias
asistencias = [
    "Acceso Remoto",
    "Carpeta Compartida",
    "Celular",
    "Computadora",
    "Conmutador",
    "Correo",
    "Documento",
    "Escáner",
    "Equipo (mouse, teclado, no break, etc.)",
    "Huella Dactilar",
    "Impresora",
    "Internet",
    "Outlook",
    "SAE",
    "Software",
    "Otro"
]

# Arreglo de usuarios
usuarios = [
    "Aaron Vázquez", "Alma Salaís", "Andrés Loredo", "Andrés Martínez", "Antonio López", "Brenda García", "Christian Betancourt", "Cristina Ramírez", "Daniel Ruiz",
    "Daniela Rodríguez", "Daniela Sánchez", "Diego Durán", "Eduardo Gomez", "Felipe Angeles", "Gabriela Vázquez", "Guadalupe Alcalá", "Guillermo Córdova",
    "Guillermo Fernández", "Irasema Lucio", "Jaqueline Rodríguez", "Javier Azuara", "Juan Antonio Mendoza", "Karina Ramírez", "Leandro Guillén", "Leslye López",
    "Luis Jardón", "Mariana Barrios", "Maripaz Corona", "Mauricio Ramírez", "Melanie Rangel", "Rodrigo Ensastiga", "Rodrigo Morales", "Usiel Silva", "Vania Ramírez",
    "Viridiana Castillo", "Yael Pérez", "Yesenia Palestina"
]

#Arreglo de empresas
empresas = [
    "CODEQUIM", "MEDICA DEL VALLE", "KILLVEC", "EXTERPLAG", "PAINTSHIELD",
]

# Arreglo del personal
sistemas = [
    "León Hernández",
    "Ismael Jiménez",
]

# Sección para añadir un Ticket
st.header("Añadir un ticket")

# Añadimos tickets vía `st.form` con algunnos widgets de entrada. Si los widgets se usan
# en un form, la app solo los devolverá cuando se haya pulsado el botón de terminar
with st.form("add_ticket_form"):
    usuario = st.selectbox("Usuario", usuarios)
    empresa = st.selectbox("Empresa", empresas)
    asistencia = st.selectbox("Asistencia", asistencias)
    solicitud = st.selectbox("Solicitud", ["Presencial", "WhatsApp", "Jefe Directo"])
    atencion = st.selectbox("Atendió", sistemas)
    descripcion = st.text_area("Descripción")
    terminar = st.form_submit_button("Terminar")

if terminar:
    # Creamos un data frame para el nuevo ticket y lo unimos al datframe de tickets existentes
    if st.session_state.df.empty:
        no_ticket = 0000
    else:
        no_ticket = int(max(st.session_state.df.ID).split("-")[1])
    #Configuramos la zona horaria de CDMX
    cdmx_tz = pytz.timezone('America/Mexico_City')
    fecha = datetime.datetime.now(cdmx_tz).strftime("%d/%m/%Y")
    hora = datetime.datetime.now(cdmx_tz).strftime("%H:%M:%S")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{no_ticket+1}",
                "FECHA": fecha,
                "HORA INICIO": hora,
                "HORA FIN": "",
                "USUARIO": usuario,
                "EMPRESA": empresa,
                "ASISTENCIA": asistencia,
                "STATUS": "Solucionado",
                "SOLICITUD": solicitud,
                "ATENDIÓ": atencion,
                "DESCRIPCIÓN": descripcion,            
            }
        ]
    )

    # Mensaje de creación de ticket
    st.write("¡Ticket registrado! Aquí los detalles de tu ticket:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)
    st.session_state.df.to_csv('tickets.csv', index=False)

# Sección para ver y editar los tickets existentes
st.header("Tickets existentes")
df_total = pd.read_csv('tickets.csv')
st.write(f"Número de tickets: `{len(df_total)}`")

st.info(
    "Recuerda cambiar el estado del ticket a solucionado una vez atendido",
    icon="✍️",
)

# Mostrar el data frame de tickets editable
# Los datos editados se devuelven como un nuevo data frame
edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "STATUS": st.column_config.SelectboxColumn(
            "STATUS",
            help="Ticket status",
            options=["Solucionado", "En Proceso"],
            required=True,
        )
    },
    # Bloqueamos la edición del resto de columnas
    disabled=["ID", "FECHA", "USUARIO", "EMPRESA", "ASISTENCIA", "HORA INICIO", "SOLICITUD", "ATENDIÓ", "DESCRIPCIÓN"],
)

# Actualizar el DataFrame en el estado de sesión y guardar en el archivo CSV si hay cambios
if not edited_df.equals(st.session_state.df):
    st.session_state.df = edited_df
    st.session_state.df.to_csv('tickets.csv', index=False)

# Sección para mostrar las métricas del área
st.header("Métricas")

col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.STATUS == "Solucionado"])
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
