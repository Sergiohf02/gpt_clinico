from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(temperature=0.2, model="gpt-4")

def diagnostico_probable(query: str) -> str:
    """
    Analiza los síntomas y sugiere diagnósticos clínicos diferenciales con probabilidad.
    Entrada típica: "fiebre, tos seca, disnea, dolor torácico"
    """
    try:
        prompt = f"""
Eres un médico especialista en medicina interna.

Analiza el caso clínico siguiente:
\"\"\"{query}\"\"\"

Y responde en español médico profesional con:

1. Diagnóstico principal (más probable)
2. Diagnósticos diferenciales (con % aproximado)
3. Pruebas recomendadas (si aplica)
4. Tratamiento empírico sugerido (si aplica)

No incluyas texto en inglés. Usa terminología clínica.
"""
        respuesta = llm.invoke(prompt)
        return respuesta.content.strip()

    except Exception as e:
        return f"Error en diagnóstico diferencial: {e}"
