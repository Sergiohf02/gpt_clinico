import os
from tavily import TavilyClient

def tavily_search(query: str) -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: Falta TAVILY_API_KEY."

    client = TavilyClient(api_key=api_key)
    try:
        result = client.search(query=query)
        # Simplificar para el agente:
        if "answer" in result and result["answer"]:
            return result["answer"]
        elif "results" in result:
            snippets = []
            for item in result["results"][:3]:  # limitar a 3
                snippets.append(f"{item.get('title')}: {item.get('content')}")
            return "\n".join(snippets)
        else:
            return str(result)
    except Exception as e:
        return f"Error al consultar Tavily: {e}"
