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

        resultados = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            nombre = props.get("nombretitu", "Desconocido")
            direccion = f"{props.get('tipovia', '')} {props.get('nombrevia', '')} {props.get('numpol', '')}".strip()
            telefono = props.get("telefono", "Sin teléfono")
            resultados.append(f"- {nombre} ({direccion}) - Tel: {telefono}")

        if resultados:
            return "Farmacias encontradas en Cáceres:\n" + "\n".join(resultados)
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

        resultados = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            situacion = props.get("situacion", "Ubicación desconocida")
            direccion = props.get("direccion", "Dirección desconocida")
            descripcion = props.get("descripcion", "")
            resultados.append(f"- {situacion} ({direccion})\n  {descripcion}")

        if resultados:
            return "Desfibriladores encontrados en Cáceres:\n" + "\n".join(resultados)
        else:
            return "No se encontraron desfibriladores disponibles."

    except Exception as e:
        return f"Error al obtener datos de desfibriladores: {str(e)}"

def get_defibrillator_tools():
    return [buscar_dea]
