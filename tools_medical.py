# tools_medical.py
from langchain.agents import tool

@tool
def generate_clinical_summary(json_str: str) -> str:
    """
    Genera una nota clínica tipo SOAP a partir de los datos (en JSON string).
    """
    import json
    try:
        data = json.loads(json_str)
    except Exception:
        return "Error: El formato de los datos no es válido."
    age = data.get("age", "No especificado")
    sex = data.get("sex", "No especificado")
    symptoms = data.get("symptoms", "No especificado")
    findings = data.get("findings", "No especificado")
    provisional_diagnosis = data.get("provisional_diagnosis", "No especificado")
    plan = data.get("plan", "No especificado")
    return (
        f"Nota clínica (SOAP):\n"
        f"Edad: {age}\nSexo: {sex}\n"
        f"Síntomas: {symptoms}\nHallazgos: {findings}\n"
        f"Diagnóstico provisional: {provisional_diagnosis}\n"
        f"Plan: {plan}"
    )


@tool
def classify_triage(symptoms: str) -> str:
    """Clasifica el nivel de urgencia médica de un caso en base a los síntomas reportados."""
    symptoms_lower = symptoms.lower()

    urgent_keywords = [
        "dolor torácico", "disnea", "pérdida de conciencia", "convulsiones",
        "sangrado abundante", "hemoptisis", "dolor abdominal intenso", "signos de sepsis"
    ]
    grave_keywords = [
        "fiebre alta", "debilidad severa", "alteración del estado mental",
        "dolor intenso", "taquicardia", "hipotensión"
    ]

    for word in urgent_keywords:
        if word in symptoms_lower:
            return "🔴 URGENTE - Derivación inmediata a urgencias"

    for word in grave_keywords:
        if word in symptoms_lower:
            return "🟠 GRAVE - Evaluación médica en menos de 24h"

    if "fiebre" in symptoms_lower or "dolor leve" in symptoms_lower or "tos" in symptoms_lower:
        return "🟡 MODERADO - Consulta médica en los próximos días"

    return "🟢 LEVE - Autocuidado o seguimiento si persiste"
