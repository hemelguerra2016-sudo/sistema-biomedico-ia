
import streamlit as st
import google.generativeai as genai

# CONFIGURAR GEMINI
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash")

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
sexo = st.selectbox(
    "Sexo biológico",
    [
        "Masculino",
        "Femenino"
    ]
)
duracion = st.selectbox(
    "Duración de síntomas",
    [
        "Menos de 24 horas",
        "1-3 días",
        "Más de 3 días"
    ]
)
antecedentes = st.multiselect(
    "Antecedentes médicos",
    [
        "Hipertensión",
        "Diabetes",
        "Asma",
        "Cardiopatías",
        "Ninguno"   ]
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

# FUNCIÓN IA + RESPALDO
def generar_orientacion(sintomas, otros, nivel, sexo, antecedentes):

    prompt = f"""
    Actúa como asistente biomédico educativo.

    Sexo:
    {sexo}

    Antecedentes:
    {antecedentes}

    Síntomas:
    {sintomas}

    Otros síntomas:
    {otros}

    Riesgo clínico:
    {nivel}

    Explica:
    - posible significado clínico
    - recomendaciones generales
    - señales de alarma

    NO diagnostiques.
    NO reemplaces al médico.
    """

    try:

        respuesta = model.generate_content(prompt)

        return respuesta.text

    except Exception:

        # RESPALDO AUTOMÁTICO

        if nivel == "rojo":

            return """
🚨 POSIBLE SITUACIÓN DE RIESGO CLÍNICO

Se recomienda acudir inmediatamente
a un servicio médico de urgencias.

Señales de alarma:
- dificultad respiratoria
- dolor intenso
- pérdida de conciencia
- empeoramiento rápido

Recomendaciones:
- no automedicarse
- mantener acompañamiento
- buscar atención inmediata

⚠️ Este sistema NO reemplaza evaluación médica profesional.
"""

        elif nivel == "amarillo":

            return """
⚠️ LOS SÍNTOMAS REQUIEREN VALORACIÓN MÉDICA

Recomendaciones generales:
- hidratación
- reposo
- monitoreo de síntomas
- consulta médica si empeoran

Señales de alarma:
- fiebre persistente
- dificultad respiratoria
- dolor progresivo

⚠️ Este sistema NO reemplaza evaluación médica profesional.
"""

        else:

            return """
✅ SÍNTOMAS LEVES

Recomendaciones generales:
- descanso
- hidratación
- observación clínica básica

Consultar médico si aparecen:
- nuevos síntomas
- empeoramiento
- fiebre persistente

⚠️ Este sistema NO reemplaza evaluación médica profesional.
"""
# BOTÓN ANALIZAR
if st.button("Analizar síntomas"):

    nivel = clasificar_riesgo(
        sintomas,
        otros
    )

    st.subheader("Resultado clínico")

    if nivel == "rojo":

        st.error("🔴 Atención médica inmediata recomendada")

    elif nivel == "amarillo":

        st.warning("🟡 Recomendable consultar médico")

    else:

        st.success("🟢 Síntomas leves")

    st.subheader("Orientación biomédica")

    respuesta = generar_orientacion(
        sintomas,
        otros,
        nivel,
        sexo,
        antecedentes
    )

    st.write(respuesta)
