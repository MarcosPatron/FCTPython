# system_agents.py

from agents import Agent, handoff
from assistant.tools import obtener_farmacias, obtener_desfibriladores

pharmacy_agent = Agent(
    name="Pharmacy Info Agent",
    instructions="Proporcionas información sobre farmacias disponibles, ubicación, horarios, etc.",
    tools=obtener_farmacias()
)

defibrillator_agent = Agent(
    name="Defibrillator Info Agent",
    instructions="Proporcionas información sobre ubicación de desfibriladores (DEA) y cómo acceder a ellos.",
    tools=obtener_desfibriladores()
)

triage_agent_instance = Agent(
    name="Triage Agent",
    instructions=(
        "Eres un agente de clasificación. Según la consulta del usuario, debes decidir si se trata de una "
        "pregunta sobre farmacias o sobre desfibriladores. Si es así, debes delegar al agente correspondiente. "
        "Responde tú mismo solo si no está claro a cuál delegar."
    ),
    handoffs=[
        handoff(pharmacy_agent),
        handoff(defibrillator_agent)
    ]
)
