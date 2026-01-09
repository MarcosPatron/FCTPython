import requests
from agents import function_tool

class HerramientasLocales:
    @staticmethod
    def _obtener_farmacias_raw():
        url = 'https://ide.caceres.es/geoserver/toponimia/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=toponimia%3Afarmacias&maxFeatures=50&outputFormat=application%2Fjson'
        try:
            respuesta = requests.get(url, timeout=100)
            respuesta.raise_for_status()
            respuesta.encoding = 'latin-1'
            datos = respuesta.json()
        except requests.exceptions.Timeout:
            return "La solicitud tardó demasiado en responder. Intenta de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return f"No se pudo obtener la información de farmacias: {e}"

        resultado = []
        for f in datos.get("features", []):
            props = f.get("properties", {})
            direccion = f"{props.get('tipovia', '')} {props.get('nombrevia', '')} {props.get('numpol', '')}".strip()
            resultado.append(f"- {props.get('nombretitu', 'Desconocido')} ({direccion})")

        if resultado:
            return "Aquí tienes algunas farmacias en Cáceres:\n" + "\n".join(resultado)
        return "No se encontraron farmacias."

    @staticmethod
    def _obtener_desfibriladores_raw():
        url = 'https://ide.caceres.es/geoserver/toponimia/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=toponimia%3Adesfibriladores&maxFeatures=50&outputFormat=application%2Fjson'
        try:
            respuesta = requests.get(url, timeout=100)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except requests.exceptions.Timeout:
            return "La solicitud tardó demasiado en responder. Intenta de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return f"No se pudo obtener la información de desfibriladores: {e}"

        resultado = []
        for d in datos.get("features", []):
            props = d.get("properties", {})
            direccion = props.get("direccion", "Dirección desconocida")
            situacion = props.get("situacion", "")
            resultado.append(f"- {situacion} ({direccion})")

        if resultado:
            return "Aquí tienes algunos desfibriladores en Cáceres:\n" + "\n".join(resultado)
        return "No se encontraron desfibriladores."

    @staticmethod
    def _obtener_estancos_raw():
        url = 'https://ide.caceres.es/geoserver/toponimia/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=toponimia%3Aestancos&maxFeatures=50&outputFormat=application%2Fjson'
        try:
            respuesta = requests.get(url, timeout=100)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except requests.exceptions.Timeout:
            return "La solicitud tardó demasiado en responder. Intenta de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return f"No se pudo obtener la información de estancos: {e}"

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

        if resultado:
            return "Aquí tienes algunos estancos en Cáceres:\n" + "\n".join(resultado)
        return "No se encontraron estancos."

    @staticmethod
    def _obtener_restaurantes_raw():
        url = 'https://ide.caceres.es/geoserver/gastrorutas/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=gastrorutas%3Arestaurantes_cc_gastroguia&maxFeatures=50&outputFormat=application%2Fjson'
        try:
            respuesta = requests.get(url, timeout=100)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except requests.exceptions.Timeout:
            return "La solicitud tardó demasiado en responder. Intenta de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return f"No se pudo obtener la información de restaurantes: {e}"

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

        if resultado:
            return "Aquí tienes algunos restaurantes en Cáceres:\n" + "\n".join(resultado)
        return "No se encontraron restaurantes."

    @staticmethod
    def _obtener_bares_cafes_raw():
        url = 'https://ide.caceres.es/geoserver/gastrorutas/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=gastrorutas%3Acafes_y_bares_gastroguia&maxFeatures=50&outputFormat=application%2Fjson'
        try:
            respuesta = requests.get(url, timeout=100)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except requests.exceptions.Timeout:
            return "La solicitud tardó demasiado en responder. Intenta de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return f"No se pudo obtener la información de cafés y bares: {e}"

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

        if resultado:
            return "Aquí tienes algunos cafés y bares en Cáceres:\n" + "\n".join(resultado)
        return "No se encontraron cafés y bares."

    @staticmethod
    def _obtener_paradas_bus_raw():
        url = 'https://ide.caceres.es/geoserver/Autobuses_Urbanos/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Autobuses_Urbanos%3AParadas&maxFeatures=250&outputFormat=application%2Fjson'
        try:
            respuesta = requests.get(url, timeout=100)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except requests.exceptions.Timeout:
            return "La solicitud tardó demasiado en responder. Intenta de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return f"No se pudo obtener la información de paradas de autobús: {e}"

        resultado = []
        for p in datos.get("features", []):
            props = p.get("properties", {})
            nombre = props.get("NOMBRE", "Parada")
            lineas = props.get("LINEAS", "Línea desconocida")
            resultado.append(f"- {nombre} | Líneas: {lineas}")

        if resultado:
            return "Aquí tienes algunas paradas de autobús en Cáceres:\n" + "\n".join(resultado)
        return "No se encontraron paradas de autobús."

    # Funciones expuestas con function_tool
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
