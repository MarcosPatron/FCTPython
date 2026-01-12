from agents import function_tool

from data_base.farmacias_repository import FarmaciasRepository
from data_base.estancos_repository import EstancosRepository
from data_base.paradas_bus_repository import ParadasBusRepository
from data_base.bares_cafes_repository import BaresCafesRepository
from data_base.restaurantes_repository import RestaurantesRepository
from data_base.desfibriladores_repository import DesfibriladoresRepository


class HerramientasLocales:

    # ========= FARMACIAS =========
    @staticmethod
    def _obtener_farmacias_raw():
        datos = FarmaciasRepository.get_all()

        if not datos:
            return "No se encontraron farmacias."

        resultado = []
        for f in datos:
            extra = f" | Tel: {f['telefono']}" if f["telefono"] else ""
            horario = f"\n  Horario: {f['horario']}" if f["horario"] else ""
            resultado.append(f"- {f['nombre']} ({f['direccion']}){extra}{horario}")

        return "Aquí tienes algunas farmacias en Cáceres:\n" + "\n".join(resultado)

    # ========= DESFIBRILADORES =========
    @staticmethod
    def _obtener_desfibriladores_raw():
        datos = DesfibriladoresRepository.get_all()

        if not datos:
            return "No se encontraron desfibriladores."

        resultado = [
            f"- {d['situacion']} ({d['direccion']})"
            for d in datos
        ]

        return "Aquí tienes algunos desfibriladores en Cáceres:\n" + "\n".join(resultado)

    # ========= ESTANCOS =========
    @staticmethod
    def _obtener_estancos_raw():
        datos = EstancosRepository.get_all()

        if not datos:
            return "No se encontraron estancos."

        resultado = []
        for e in datos:
            extra = f" | Web: {e['web']}" if e["web"] else ""
            resultado.append(f"- {e['nombre']} ({e['direccion']}){extra}")

        return "Aquí tienes algunos estancos en Cáceres:\n" + "\n".join(resultado)

    # ========= RESTAURANTES =========
    @staticmethod
    def _obtener_restaurantes_raw():
        datos = RestaurantesRepository.get_all()

        if not datos:
            return "No se encontraron restaurantes."

        resultado = []
        for r in datos:
            extra = f" | Tel: {r['telefono']}" if r["telefono"] else ""
            if r["web"]:
                extra += f" | Web: {r['web']}"
            resultado.append(f"- {r['nombre']} ({r['direccion']}){extra}")

        return "Aquí tienes algunos restaurantes en Cáceres:\n" + "\n".join(resultado)

    # ========= BARES / CAFÉS =========
    @staticmethod
    def _obtener_bares_cafes_raw():
        datos = BaresCafesRepository.get_all()

        if not datos:
            return "No se encontraron cafés y bares."

        resultado = []
        for b in datos:
            extra = f" | Tel: {b['telefono']}" if b["telefono"] else ""
            if b["web"]:
                extra += f" | Web: {b['web']}"
            resultado.append(f"- {b['nombre']} ({b['direccion']}){extra}")

        return "Aquí tienes algunos cafés y bares en Cáceres:\n" + "\n".join(resultado)

    # ========= PARADAS BUS =========
    @staticmethod
    def _obtener_paradas_bus_raw():
        datos = ParadasBusRepository.get_all()

        if not datos:
            return "No se encontraron paradas de autobús."

        resultado = [
            f"- {p['direccion']} | Líneas: {p['lineas']} | Tiempo real: {p['tiempopaso']}"
            for p in datos
        ]

        return "Aquí tienes algunas paradas de autobús en Cáceres:\n" + "\n".join(resultado)

    # ========= function_tool =========
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
