from google.adk.agents import Agent
from src.tools.avaliar_escola import classificar_prioridade_escola

def criar_agente_educacao() -> Agent:
    """
    Inicializa e configura o agente ADK.
    """
    agente = Agent(
        name="auditor_infraestrutura_escolar",  # <-- CORREÇÃO: Sem espaços, formato snake_case
        model="gemini-2.5-flash",
        instruction=(
            "Você é um analista de dados educacionais focado em políticas públicas. "
            "Sua função é auxiliar na tomada de decisão sobre alocação de recursos em escolas. "
            "Ao receber os dados de uma escola (alunos, internet e nota de infraestrutura), "
            "você deve OBRIGATORIAMENTE utilizar a ferramenta 'classificar_prioridade_escola' "
            "para determinar o nível de necessidade de investimento. "
            "Após o uso da ferramenta, explique a classificação gerada de forma clara e profissional."
        ),
        tools=[classificar_prioridade_escola]
    )

    return agente