
import streamlit as st
import google.generativeai as genai

# CONFIGURAR GEMINI
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# CONFIGURACIÓN STREAMLIT
st.set_page_config(page_title="Sistema Biomédico IA")

st.title("🩺 Sistema IA de Preorientación Biomédica")

st.write("""
Aplicación educativa de apoyo preliminar
para clasificación básica de síntomas.
""")

# LISTA DE SÍNTOMAS
opciones_sintomas = [
    "dolor de pecho",
    "dificultad respiratoria",
    "fiebre",
    "dolor de cabeza",
    "mareo",
    "vomito",
    "tos",
    "cansancio",
    "desmayo",
    "convulsiones"
]

# FORMULARIO
edad = st.number_input(
    "Edad",
    min_value=0,
    max_value=120
)

sintomas = st.multiselect(
    "Seleccione síntomas",
    opciones_sintomas
)

otros = st.text_area(
    "Otros síntomas"
)

# FUNCIÓN BIOMÉDICA
def clasificar_riesgo(sintomas, otros):

    texto = otros.lower()

    sintomas_rojos = [
        "dolor de pecho",
        "dificultad respiratoria",
        "desmayo",
        "convulsiones"
    ]

    sintomas_amarillos = [
        "fiebre",
        "dolor de cabeza",
        "mareo",
        "vomito",
        "tos",
        "cansancio"
    ]

    # Revisar síntomas seleccionados
    for sintoma in sintomas:

        if sintoma in sintomas_rojos:
            return "rojo"

    for sintoma in sintomas:

        if sintoma in sintomas_amarillos:
            return "amarillo"

    # Revisar texto libre
    if (
        "no puedo respirar" in texto or
        "me falta el aire" in texto or
        "me duele el pecho" in texto
    ):
        return "rojo"

    return "verde"

# FUNCIÓN IA
def generar_orientacion(sintomas, otros, nivel):

    prompt = f"""
    Actúa como un asistente biomédico educativo.

    Edad:
    {edad}

    Síntomas seleccionados:
    {sintomas}

    Otros síntomas:
    {otros}

    Clasificación:
    {nivel}

    Genera:
    - explicación breve
    - recomendaciones generales
    - señales de alarma
    - advertencia médica final

    IMPORTANTE:
    - No diagnosticar enfermedades
    - No formular tratamientos
    - No reemplazar médicos
    """

    respuesta = model.generate_content(prompt)

    return respuesta.text

# BOTÓN
if st.button("Analizar síntomas"):

    nivel = clasificar_riesgo(
        sintomas,
        otros
    )

    st.subheader("Resultado clínico")

    if nivel == "rojo":

        st.error(
            "🔴 Atención médica inmediata recomendada"
        )

    elif nivel == "amarillo":

        st.warning(
            "🟡 Recomendable consultar médico"
        )

    else:

        st.success(
            "🟢 Síntomas leves"
        )

    st.subheader("Orientación biomédica")

    respuesta = generar_orientacion(
        sintomas,
        otros,
        nivel
    )

    st.write(respuesta)

    st.info("""
    Esta aplicación NO reemplaza valoración
    médica profesional.
    Es únicamente una herramienta educativa.
    """)
