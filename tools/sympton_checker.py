# tools/symptom_checker.py
import requests

API_URL = "https://tudominio.com/symptoms"  # Usa tu link real

def get_diagnosis_from_api(symptom_description: str) -> str:
    payload = {"symptoms": symptom_description}

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return f"Diagnóstico posible: {data.get('diagnosis', 'No se encontró diagnóstico')}"
    except requests.exceptions.RequestException as e:
        return f"Error al consultar la API médica: {e}"
