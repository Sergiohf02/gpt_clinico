# tools/triage_clinico.py

from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(temperature=0.2, model="gpt-4")

def evaluar_news2(query: str) -> str:
    """
    Entrada sugerida:
    - "fc=118 fr=26 temp=38.7 sat=89 pas=95"
    - "Paciente con FC 120, FR 30, SatO2 88%, Temp 39°C, PAS 92"
    """
    try:
        prompt = f'''
Eres un médico de urgencias. Evalúa el nivel de riesgo clínico de un paciente según sus signos vitales, usando como base la escala NEWS2.

Signos vitales proporcionados:
\"\"\"{query}\"\"\"

Proporciona:
- Puntaje estimado (aproximado si no se puede calcular exacto)
- Nivel de riesgo (BAJO, MODERADO o ALTO)
- Justificación médica breve
- Recomendación clínica (ej. observación, derivación, traslado)

Responde de forma clara y estructurada.
'''
        respuesta = llm.invoke(prompt)
        return respuesta.content.strip()

    except Exception as e:
        return f"Error al generar triage con LLM: {e}"
