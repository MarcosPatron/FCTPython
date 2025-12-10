# assistant/system_agents.py

from agents import Agent, handoff
from assistant.tools import HerramientasLocales

pharmacy_agent = Agent(
    name="Pharmacy Info Agent",
    instructions="Proporcionas información sobre farmacias disponibles, ubicación, horarios, etc.",
    tools=[HerramientasLocales.obtener_farmacias]
)

defibrillator_agent = Agent(
    name="Defibrillator Info Agent",
    instructions="Proporcionas información sobre ubicación de desfibriladores (DEA) y cómo acceder a ellos.",
    tools=[HerramientasLocales.obtener_desfibriladores]
)

tobacco_shop_agent = Agent(
    name="Tobacco Shop Info Agent",
    instructions="Proporcionas información sobre estancos disponibles, ubicación, teléfono y página web si están disponibles.",
    tools=[HerramientasLocales.obtener_estancos]
)

restaurant_agent = Agent(
    name="Restaurant Info Agent",
    instructions="Proporcionas información sobre restaurantes en Cáceres, incluyendo dirección, teléfono y página web.",
    tools=[HerramientasLocales.obtener_restaurantes]
)

cafe_bar_agent = Agent(
    name="Cafe and Bar Info Agent",
    instructions="Proporcionas información sobre cafés y bares en Cáceres, incluyendo dirección, teléfono y página web.",
    tools=[HerramientasLocales.obtener_bares_cafes]
)

bus_stop_agent = Agent(
    name="Bus Stop Info Agent",
    instructions="Proporcionas información sobre paradas de autobuses urbanos, incluyendo nombres de parada y las líneas que pasan por ellas.",
    tools=[HerramientasLocales.obtener_paradas_bus] # Herramientas que tiene disponible
)

# Generar un asistente
triage_agent_instance = Agent(
    name="Triage Agent", # Nombre del agente
    instructions=( # Instrucciones
        "Eres un agente de clasificación. Según la consulta del usuario, debes decidir si se trata de una "
        "pregunta sobre farmacias, desfibriladores, estancos, restaurantes, bares/cafés o paradas de autobús. "
        "No le digas al usuario que tipo de informacion tienes."
        "Debes delegar al agente correspondiente. Responde tú mismo solo si no está claro a cuál delegar."
        "Proporciona a el resto de agentes las coordenadas para que tengan mas contexto de la situacion del usuario"
    ),
    handoffs=[ # Agentes a los que delega
        handoff(pharmacy_agent),
        handoff(defibrillator_agent),
        handoff(tobacco_shop_agent),
        handoff(restaurant_agent),
        handoff(cafe_bar_agent),
        handoff(bus_stop_agent)
    ]
)
