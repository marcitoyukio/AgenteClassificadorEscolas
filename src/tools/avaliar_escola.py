import os
import joblib
from google.adk.tools import FunctionTool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'classificador_escolas.joblib')

def classificar_prioridade_escola_func(qt_mat_bas: int, in_internet: int, in_biblioteca: int, in_esgoto_rede: int) -> str:
    """
    Avalia a prioridade de investimento de uma escola com base nos indicadores oficiais do INEP.
    Os parâmetros de infraestrutura (in_internet, in_biblioteca, in_esgoto_rede) devem ser numéricos: 1 (possui) ou 0 (não possui).
    Retorna a classificação de prioridade de investimento ('Alta', 'Media', 'Baixa').
    """
    try:
        modelo = joblib.load(MODEL_PATH)
        entrada = [[qt_mat_bas, in_internet, in_biblioteca, in_esgoto_rede]]
        predicao = modelo.predict(entrada)
        return predicao[0]
    except FileNotFoundError:
        return "Erro interno: Modelo não encontrado."

# Envolvem a função na classe oficial do framework
classificar_prioridade_escola = FunctionTool(classificar_prioridade_escola_func)