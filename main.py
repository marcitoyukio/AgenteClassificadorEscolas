import os
import asyncio
from dotenv import load_dotenv
import warnings
import contextlib
from src.agent.orquestrador import criar_agente_educacao
from google.adk.runners import InMemoryRunner

# Silencia avisos do ADK
warnings.filterwarnings("ignore")

async def chat_interativo():
    # Carrega as variáveis de ambiente
    load_dotenv()

    print("===================================================")
    print("🤖 Auditor Escolar ADK Inicializado")
    print("💡 Digite 'sair' a qualquer momento para encerrar.")
    print("===================================================\n")

    agente = criar_agente_educacao()
    runner = InMemoryRunner(agent=agente)

    # Inicia chat
    while True:
        pergunta = input("\n[Você]: ")

        # Condição de saída do chat
        if pergunta.strip().lower() in ['sair', 'exit', 'quit']:
            print("\nEncerrando o agente. Até logo!")
            break

        if not pergunta.strip():
            continue

        print("Pensando...")

        try:
            with open(os.devnull, 'w') as limpa_log:
                with contextlib.redirect_stdout(limpa_log):
                    eventos = await runner.run_debug(pergunta)

            # Extrai o texto limpo do último evento
            texto_final = eventos[-1].content.parts[0].text
            print(f"\n[Agente]:\n{texto_final}")

        except Exception as e:
            print(f"\n[Erro na comunicação]: {e}")

def main():
    asyncio.run(chat_interativo())

if __name__ == "__main__":
    main()