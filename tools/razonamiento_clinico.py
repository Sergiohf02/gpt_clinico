from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(temperature=0.1, model="gpt-4")

def razonamiento_soap(query: str) -> str:
    try:
        prompt = f"""
Eres un médico clínico. Redacta una nota médica tipo SOAP basada exclusivamente en la siguiente información:

\"\"\"{query}\"\"\"

Formato:
- SUBJETIVO: Solo síntomas que refiere el paciente, no valores medidos (ej: "refiere fiebre", "tiene tos", "siente dolor").
- OBJETIVO: Solo datos medidos u observables por el médico (temperatura, FC, peso, SatO2, etc.).
- ANÁLISIS: Juicio clínico razonado, sin asumir diagnósticos que no se desprendan directamente.
- PLAN: Sugerencias razonables (pruebas, tratamiento sintomático, seguimiento).

No repitas síntomas en más de una sección. No menciones enfermedades que no aparecen en los datos. Escribe de forma breve, profesional y en español técnico.
"""


        respuesta = llm.invoke(prompt)
        return respuesta.content.strip()

    except Exception as e:
        return f"Error al generar razonamiento clínico: {e}"
