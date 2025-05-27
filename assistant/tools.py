import requests
from agents import function_tool

class HerramientasLocales:
    @staticmethod
    def _obtener_farmacias_raw():
        url = 'https://ide.caceres.es/geoserver/toponimia/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=toponimia%3Afarmacias&maxFeatures=50&outputFormat=application%2Fjson'
        respuesta = requests.get(url)
        respuesta.encoding = 'latin-1'
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultado = []
            for f in datos.get("features", []):
                props = f.get("properties", {})
                direccion = f"{props.get('tipovia', '')} {props.get('nombrevia', '')} {props.get('numpol', '')}"
                resultado.append(f"- {props.get('nombretitu', 'Desconocido')} ({direccion.strip()})")
            return "Aquí tienes algunas farmacias en Cáceres:\n" + "\n".join(resultado)
        return "No se pudo obtener la información de farmacias."

    @staticmethod
    def _obtener_desfibriladores_raw():
        url = 'https://ide.caceres.es/geoserver/toponimia/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=toponimia%3Adesfibriladores&maxFeatures=50&outputFormat=application%2Fjson'
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultado = []
            for d in datos.get("features", []):
                props = d.get("properties", {})
                direccion = props.get("direccion", "Dirección desconocida")
                situacion = props.get("situacion", "")
                resultado.append(f"- {situacion} ({direccion})")
            return "Aquí tienes algunos desfibriladores en Cáceres:\n" + "\n".join(resultado)
        return "No se pudo obtener la información de desfibriladores."

    @staticmethod
    @function_tool
    def obtener_farmacias():
        return HerramientasLocales._obtener_farmacias_raw()

    @staticmethod
    @function_tool
    def obtener_desfibriladores():
        return HerramientasLocales._obtener_desfibriladores_raw()
