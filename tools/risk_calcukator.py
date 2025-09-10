# tools/risk_calculator.py
def calculate_imc(query: str) -> str:
    # Espera entrada como: "peso=70 altura=1.75"
    try:
        parts = dict(p.split("=") for p in query.split())
        peso = float(parts.get("peso", 0))
        altura = float(parts.get("altura", 0))
        if peso == 0 or altura == 0:
            return "Falta peso o altura"
        imc = peso / (altura ** 2)
        categoria = (
            "Bajo peso" if imc < 18.5 else
            "Normal" if imc < 25 else
            "Sobrepeso" if imc < 30 else
            "Obesidad"
        )
        return f"Tu IMC es {imc:.2f} → {categoria}"
    except:
        return "Formato incorrecto. Usa: 'peso=70 altura=1.75'"
