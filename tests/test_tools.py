from agents import Agent, Runner
from assistant import get_pharmacy_tools, get_defibrillator_tools

def test_buscar_farmacia():
    agent = Agent(
        name="Agente de Farmacias",
        instructions="Proporciona información sobre farmacias disponibles en Cáceres.",
        tools=get_pharmacy_tools()
    )
    result = Runner.run_sync(agent, "¿Dónde hay farmacias en Cáceres?")
    print("Resultado buscar_farmacia:")
    print(result.final_output)
    print("-" * 50)

def test_buscar_dea():
    agent = Agent(
        name="Agente de Desfibriladores",
        instructions="Proporciona información sobre desfibriladores públicos (DEA) disponibles en Cáceres.",
        tools=get_defibrillator_tools()
    )
    result = Runner.run_sync(agent, "¿Dónde hay desfibriladores en Cáceres?")
    print("Resultado buscar_dea:")
    print(result.final_output)
    print("-" * 50)

if __name__ == "__main__":
    test_buscar_farmacia()
    test_buscar_dea()
