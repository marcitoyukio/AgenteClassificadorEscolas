import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Mapeamento de caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'censo_escolar_2022.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'classificador_escolas.joblib')

def processar_dados_censo(caminho_csv):
    """Lê o CSV de forma otimizada e trata os dados do INEP."""
    colunas_interesse = ['CO_ENTIDADE', 'QT_MAT_BAS', 'IN_INTERNET', 'IN_BIBLIOTECA', 'IN_ESGOTO_REDE_PUBLICA']

    try:
        df = pd.read_csv(
            caminho_csv,
            sep=';',
            encoding='latin1',
            usecols=colunas_interesse,
        )
    except Exception as e:
        print(f"Erro na leitura. Verifique se o arquivo está na pasta certa: {e}")
        return None

    #Trata valores nulos e ajusta a tipagem
    df = df.fillna({'IN_INTERNET': 0, 'IN_BIBLIOTECA': 0, 'IN_ESGOTO_REDE_PUBLICA': 0, 'QT_MAT_BAS': 0})

    colunas_infra = ['IN_INTERNET', 'IN_BIBLIOTECA', 'IN_ESGOTO_REDE_PUBLICA']
    df[colunas_infra] = df[colunas_infra].astype(int)
    df['QT_MAT_BAS'] = df['QT_MAT_BAS'].astype(int)

    # Regra de negócio (Target)
    def classificar(row):
        score_infra = row['IN_INTERNET'] + row['IN_BIBLIOTECA'] + row['IN_ESGOTO_REDE_PUBLICA']
        if score_infra <= 1: return 'Alta'
        elif score_infra == 2: return 'Media'
        else: return 'Baixa'

    df['PRIORIDADE_ALVO'] = df.apply(classificar, axis=1)
    return df

def executar_pipeline():
    """Orquestra a ingestão, treinamento e exportação do modelo."""
    if not os.path.exists(CSV_PATH):
        print(f"Erro: Arquivo não encontrado no caminho:\n{CSV_PATH}")
        return

    df = processar_dados_censo(CSV_PATH)
    if df is None:
        return

    print("Separando dados em Treino e Teste...")
    X = df[['QT_MAT_BAS', 'IN_INTERNET', 'IN_BIBLIOTECA', 'IN_ESGOTO_REDE_PUBLICA']]
    y = df['PRIORIDADE_ALVO']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Treinando o modelo de ML...")
    modelo = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    modelo.fit(X_train, y_train)

    # Avaliação
    acuracia = accuracy_score(y_test, modelo.predict(X_test))
    print(f"Acurácia do modelo nos dados de teste: {acuracia * 100:.2f}%")

    # Exportação
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(modelo, MODEL_PATH)
    print(f"Sucesso! O artefato final do modelo foi salvo em:\n{MODEL_PATH}")

if __name__ == "__main__":
    executar_pipeline()