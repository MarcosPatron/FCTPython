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
                direccion = f"{props.get('tipovia', '')} {props.get('nombrevia', '')} {props.get('numpol', '')}".strip()
                resultado.append(f"- {props.get('nombretitu', 'Desconocido')} ({direccion})")
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
    def _obtener_estancos_raw():
        url = 'http://ide.caceres.es/geoserver/toponimia/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=toponimia%3Aestancos&maxFeatures=50&outputFormat=application%2Fjson'
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultado = []
            for e in datos.get("features", []):
                props = e.get("properties", {})
                direccion = f"{props.get('tipovia', '')} {props.get('nombrevia', '')} {props.get('numpol', '')}".strip()
                telefono = props.get("telefono", "Sin teléfono")
                web = props.get("web", "")
                extra = f" | Tel: {telefono}"
                if web:
                    extra += f" | Web: {web}"
                resultado.append(f"- {props.get('nombre', 'Estanco')} ({direccion}){extra}")
            return "Aquí tienes algunos estancos en Cáceres:\n" + "\n".join(resultado)
        return "No se pudo obtener la información de estancos."

    @staticmethod
    def _obtener_restaurantes_raw():
        url = 'https://ide.caceres.es/geoserver/gastrorutas/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=gastrorutas%3Arestaurantes_cc_gastroguia&maxFeatures=50&outputFormat=application%2Fjson'
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultado = []
            for r in datos.get("features", []):
                props = r.get("properties", {})
                nombre = props.get("nombre", "Restaurante")
                direccion = props.get("direccion", "Dirección desconocida")
                telefono = props.get("telefono", "Sin teléfono")
                web = props.get("web", "")
                extra = f" | Tel: {telefono}"
                if web:
                    extra += f" | Web: {web}"
                resultado.append(f"- {nombre} ({direccion}){extra}")
            return "Aquí tienes algunos restaurantes en Cáceres:\n" + "\n".join(resultado)
        return "No se pudo obtener la información de restaurantes."

    @staticmethod
    def _obtener_bares_cafes_raw():
        url = 'https://ide.caceres.es/geoserver/gastrorutas/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=gastrorutas%3Acafes_y_bares_gastroguia&maxFeatures=50&outputFormat=application%2Fjson'
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultado = []
            for b in datos.get("features", []):
                props = b.get("properties", {})
                nombre = props.get("nombre", "Café/Bar")
                direccion = props.get("direccion", "Dirección desconocida")
                telefono = props.get("telefono", "Sin teléfono")
                web = props.get("web", "")
                extra = f" | Tel: {telefono}"
                if web:
                    extra += f" | Web: {web}"
                resultado.append(f"- {nombre} ({direccion}){extra}")
            return "Aquí tienes algunos cafés y bares en Cáceres:\n" + "\n".join(resultado)
        return "No se pudo obtener la información de cafés y bares."

    @staticmethod
    def _obtener_paradas_bus_raw():
        url = 'https://ide.caceres.es/geoserver/Autobuses_Urbanos/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Autobuses_Urbanos%3AParadas&maxFeatures=250&outputFormat=application%2Fjson'
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            resultado = []
            for p in datos.get("features", []):
                props = p.get("properties", {})
                nombre = props.get("NOMBRE", "Parada")
                lineas = props.get("LINEAS", "Línea desconocida")
                resultado.append(f"- {nombre} | Líneas: {lineas}")
            return "Aquí tienes algunas paradas de autobús en Cáceres:\n" + "\n".join(resultado)
        return "No se pudo obtener la información de paradas de autobús."

    @staticmethod
    @function_tool
    def obtener_farmacias():
        return HerramientasLocales._obtener_farmacias_raw()

    @staticmethod
    @function_tool
    def obtener_desfibriladores():
        return HerramientasLocales._obtener_desfibriladores_raw()

    @staticmethod
    @function_tool
    def obtener_estancos():
        return HerramientasLocales._obtener_estancos_raw()

    @staticmethod
    @function_tool
    def obtener_restaurantes():
        return HerramientasLocales._obtener_restaurantes_raw()

    @staticmethod
    @function_tool
    def obtener_bares_cafes():
        return HerramientasLocales._obtener_bares_cafes_raw()

    @staticmethod
    @function_tool
    def obtener_paradas_bus():
        return HerramientasLocales._obtener_paradas_bus_raw()
