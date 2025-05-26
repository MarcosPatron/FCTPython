import requests
from agents import function_tool

# -------------------- FARMACIAS --------------------

@function_tool
def buscar_farmacia() -> str:
    """Devuelve una lista de farmacias disponibles en Cáceres."""
    url = "https://ide.caceres.es/geoserver/toponimia/ows"
    params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": "toponimia:farmacias",
        "maxFeatures": 50,
        "outputFormat": "application/json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        resultados = [
            feature["properties"].get("descripcion", "")
            for feature in data.get("features", [])
        ]

        if resultados:
            return "Farmacias encontradas:\n- " + "\n- ".join(resultados)
        else:
            return "No se encontraron farmacias disponibles."

    except Exception as e:
        return f"Error al obtener datos de farmacias: {str(e)}"

def get_pharmacy_tools():
    return [buscar_farmacia]

# ----------------- DESFIBRILADORES -----------------

@function_tool
def buscar_dea() -> str:
    """Devuelve una lista de desfibriladores públicos (DEA) disponibles en Cáceres."""
    url = "https://ide.caceres.es/geoserver/toponimia/ows"
    params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": "toponimia:desfibriladores",
        "maxFeatures": 100,
        "outputFormat": "application/json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        resultados = [
            feature["properties"].get("descripcion", "")
            for feature in data.get("features", [])
        ]

        if resultados:
            return "Desfibriladores encontrados:\n- " + "\n- ".join(resultados)
        else:
            return "No se encontraron desfibriladores disponibles."

    except Exception as e:
        return f"Error al obtener datos de desfibriladores: {str(e)}"

def get_defibrillator_tools():
    return [buscar_dea]
