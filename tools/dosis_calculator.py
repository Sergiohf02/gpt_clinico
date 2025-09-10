# tools/dosis_avanzada.py

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(temperature=0.2, model="gpt-4")

def calcular_dosis_medicamento(query: str) -> str:
    """
    Entrada esperada: lenguaje natural o clave=valor como:
    - "medicamento=paracetamol peso=20 edad=5 via=oral"
    - "Quiero saber la dosis oral de ibuprofeno para niño de 18 kg y 6 años"
    """
    try:
        prompt = f"""
Eres un médico farmacólogo experto. Calcula la dosis apropiada del medicamento en base a la siguiente descripción:

\"\"\"{query}\"\"\"

Incluye:
- Nombre del medicamento
- Vía de administración
- Dosis exacta en mg
- Volumen aproximado si se proporciona concentración (ej. 100mg/5ml)
- Frecuencia de administración
- Máximo diario recomendado

La respuesta debe ser clara, médica y concisa.
"""
        respuesta = llm.invoke(prompt)
        return respuesta.content.strip()

    except Exception as e:
        return f"Error al calcular dosis con LLM: {e}"
