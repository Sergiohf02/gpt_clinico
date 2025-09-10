import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from tools.dosis_calculator import calcular_dosis_medicamento
from tools.triage_level import evaluar_news2
from tools.razonamiento_clinico import razonamiento_soap
from tools.diagnostico_diferencial import diagnostico_probable
from tools.web_search import tavily_search

load_dotenv()
<<<<<<< HEAD
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("TAVILY_API_KEY:", os.getenv("TAVILY_API_KEY"))
=======
>>>>>>> 3900313df3b5e3120dea498921d5fbad6d2430f4

# Configuración de página
st.set_page_config(page_title="🧠 Asistente Clínico Avanzado", layout="wide")
st.markdown("""
<style>
    .main {background-color: #f4f6f7; padding: 2rem;}
    h1 {color: #3c3c3c;}
</style>
""", unsafe_allow_html=True)

# Sidebar con datos del paciente
st.sidebar.title("📋 Datos del Paciente")
if "paciente" not in st.session_state:
    st.session_state.paciente = {
        "nombre": "",
        "edad": 0,
        "peso": 0.0,
        "sexo": "Masculino",
        "id": ""
    }

reset = st.sidebar.button("🔄 Nueva consulta")
if reset:
    st.session_state.paciente = {
        "nombre": "",
        "edad": 0,
        "peso": 0.0,
        "sexo": "Masculino",
        "id": ""
    }
    st.experimental_rerun()

paciente = st.session_state.paciente

# Protege los valores por defecto
peso_default = paciente["peso"] if paciente["peso"] >= 0.1 else 70.0
edad_default = paciente["edad"] if paciente["edad"] >= 0 else 30

paciente["nombre"] = st.sidebar.text_input("Nombre completo", paciente["nombre"])
paciente["edad"] = st.sidebar.number_input("Edad", 0, 120, edad_default)
paciente["peso"] = st.sidebar.number_input("Peso (kg)", 0.1, 200.0, peso_default)
paciente["sexo"] = st.sidebar.selectbox("Sexo", ["Masculino", "Femenino", "Otro"], index=["Masculino", "Femenino", "Otro"].index(paciente["sexo"]))
paciente["id"] = st.sidebar.text_input("ID Clínico", paciente["id"])


# Inicializar modelo y herramientas
llm = ChatOpenAI(temperature=0.3, model="gpt-4")
herramientas_medicas = [
    Tool(name="DosisAvanzada", func=calcular_dosis_medicamento, description="Calcula dosis precisa basada en peso, edad y vía de administración"),
    Tool(name="TriageNEWS2", func=evaluar_news2, description="Evalúa urgencia clínica según signos vitales con escala NEWS2"),
    Tool(name="RazonamientoSOAP", func=razonamiento_soap, description="Genera análisis clínico estructurado tipo SOAP"),
    Tool(name="DxDiferencial", func=diagnostico_probable, description="Sugerencia de diagnósticos probables con % basado en síntomas"),
    Tool(name="BusquedaWeb", func=tavily_search, description="Realiza una búsqueda en la web médica para ampliar el contexto clínico")
]
agente_clinico = initialize_agent(herramientas_medicas, llm, agent="zero-shot-react-description", verbose=True)

# UI principal
st.title("🧠 Asistente Clínico con Agente LLM")
st.write("Introduce un caso clínico o consulta médica. El sistema usará herramientas clínicas especializadas para responder.")

col1, col2 = st.columns([2, 1])

with col1:
    consulta = st.text_area("🩺 Describe el caso clínico, síntomas, signos o preguntas:", height=200)
    if st.button("🔍 Analizar consulta"):
        with st.spinner("Analizando con herramientas médicas..."):
            contexto_paciente = f"Paciente: {paciente['nombre']}, Edad: {paciente['edad']} años, Peso: {paciente['peso']} kg, Sexo: {paciente['sexo']}."
            query_con_contexto = f"{contexto_paciente} {consulta}"
            resultado = agente_clinico.run(query_con_contexto)
            st.success("✅ Análisis completo")
            st.markdown(f"**📄 Resultado para {paciente['nombre']} ({paciente['id']}):**\n\n{resultado}")

            # Guardar historial JSON
            historial_dir = "historial"
            os.makedirs(historial_dir, exist_ok=True)
            registro = {
                "id": paciente["id"],
                "nombre": paciente["nombre"],
                "edad": paciente["edad"],
                "peso": paciente["peso"],
                "sexo": paciente["sexo"],
                "consulta": consulta,
                "respuesta_agente": resultado
            }
            with open(os.path.join(historial_dir, f"{paciente['id']}.json"), "w", encoding="utf-8") as f:
                json.dump(registro, f, ensure_ascii=False, indent=4)

with col2:
    st.markdown("### 🧰 Herramientas disponibles")
    with st.expander("💊 DosisAvanzada"):
        st.markdown("Calcula dosis exactas según edad, peso y concentración del medicamento.")
    with st.expander("📊 TriageNEWS2"):
        st.markdown("Evalúa el riesgo clínico de un paciente a partir de sus signos vitales usando la escala NEWS2.")
    with st.expander("🧠 RazonamientoSOAP"):
        st.markdown("Genera notas clínicas estructuradas tipo SOAP: Subjetivo, Objetivo, Análisis y Plan.")
    with st.expander("🔬 DxDiferencial"):
        st.markdown("Sugiere posibles diagnósticos basados en los síntomas proporcionados, con estimación de probabilidad.")
    with st.expander("🌐 BusquedaWeb"):
        st.markdown("Realiza una búsqueda web médica cuando se requiere contexto actualizado sobre enfermedades o tratamientos.")

    st.info("Las herramientas se activan automáticamente según el contenido de tu consulta.")

# Mostrar historial
if os.path.exists("historial"):
    st.sidebar.markdown("### 📁 Historial de consultas")
    filtro = st.sidebar.text_input("🔎 Filtrar por nombre o ID")
    for archivo in sorted(os.listdir("historial")):
        if archivo.endswith(".json"):
            with open(os.path.join("historial", archivo), encoding="utf-8") as f:
                caso = json.load(f)
            if filtro.lower() in caso["id"].lower() or filtro.lower() in caso["nombre"].lower():
                with st.sidebar.expander(f"{caso['id']} - {caso['nombre']}"):
                    st.markdown(f"**Edad:** {caso['edad']}  ")
                    st.markdown(f"**Peso:** {caso['peso']} kg")
                    st.markdown(f"**Sexo:** {caso['sexo']}")
                    st.markdown(f"**Consulta:** {caso['consulta']}")
                    st.markdown(f"**Respuesta:** {caso['respuesta_agente']}")