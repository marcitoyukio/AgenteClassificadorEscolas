# Agente Auditor de Infraestrutura Escolar

Este projeto foi desenvolvido como parte de um desafio técnico de engenharia de software e inteligência artificial. O ecossistema une um **Agente de IA (LLM)** construído com o framework **Google ADK** à precisão preditiva do **Machine Learning Clássico (Scikit-Learn)**, consumindo dados reais do **Censo Escolar da Educação Básica (INEP)**.

<img width="1918" height="1010" alt="preview" src="https://github.com/user-attachments/assets/62697fa4-1290-47bb-83f0-774f9c9cfb12" />

---

## Objetivo

O agente atua como um **Auditor de Infraestrutura Escolar**. O objetivo principal é avaliar a infraestrutura de escolas públicas brasileiras e **classificar** a prioridade de receber investimentos públicos através de uma **interface conversacional (Chat no Terminal)**.

Em vez de operar sistemas complexos de predição, o usuário interage em linguagem natural. O agente identifica a intenção, extrai as variáveis da escola, aciona o modelo de Machine Learning de forma silenciosa e assíncrona, interpreta o resultado matemático e devolve um parecer técnico estruturado e humanizado.

---

## Tecnologias usadas

* **Linguagem Principal:** Python 3.14
* **Orquestração de Agentes:** Google ADK (Agent Development Kit)
* **Modelagem Preditiva:** Scikit-Learn (`RandomForestClassifier`)
* **Engenharia de Dados:** Pandas & Joblib
* **Orquestração de Runtime:** Asyncio (I/O assíncrono nativo)

---

## Como usar

Siga o passo a passo completo abaixo para configurar o ambiente, gerar as credenciais, preparar os dados e rodar o ecossistema localmente:

### Passo 1: Instalar as Dependências
Abra o terminal na raiz do seu projeto e execute os seguintes comandos para configurar o seu ambiente virtual (`venv`) e instalar todas as bibliotecas necessárias para o agente e o modelo de Machine Learning:

```bash
# 1. Criar o ambiente virtual (caso ainda não tenha criado)
python -m venv .venv

#2. Ativar o ambiente virtual:
No Windows (PowerShell/CMD):
    .venv\Scripts\activate
   
No macOS e Linux:
    source .venv/bin/activate

# 3. Instalar os pacotes necessários
pip install -r requirements.txt
```

### Passo 2: Gerar a Chave de API do Gemini
O agente utiliza os modelos fundacionais do Google para interpretar as perguntas em linguagem natural. Para obter sua credencial gratuita:
1. Acesse o portal do **Google AI Studio** em: [aistudio.google.com](https://aistudio.google.com/)
2. Faça login com a sua conta Google.
3. No menu lateral ou painel principal, clique no botão **"Get API key"** (Obter chave de API).
4. Clique em **"Create API key"** (Criar chave de API), selecione ou crie um projeto padrão e copie o código alfanumérico gerado (ex: `AIzaSy...`).

### Passo 3: Configurar Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do seu projeto e insira a chave de API que você acabou de copiar no passo anterior:
```text
GOOGLE_API_KEY="COLE_SUA_CHAVE_API_AQUI"
```

### Passo 4: Baixar a Base de Dados do Kaggle
Para que o modelo seja treinado com dados governamentais realistas:
1. Acesse a plataforma do **Kaggle** (crie uma conta gratuita se necessário). 
2. Faça o download do conjunto de dados unificado do [Censo Escolar 2022](https://www.kaggle.com/datasets/hugobovaretohorsth/censo-escolar-2022-brazil?resource=download) - arquivo compactado (.zip).
3. Extraia o arquivo.
4. Localize o arquivo CSV principal do censo, renomeie-o exatamente para **`censo_escolar_2022.csv`**.
5. Mova este arquivo para dentro do diretório do projeto no caminho: `data/raw/` (crie as pastas se elas não existirem).

### Passo 5: Executar o Treinamento do Modelo Preditivo
Antes de ligar a interface do agente, você precisa gerar o arquivo binário que contém as regras matemáticas que o algoritmo aprendeu. Execute o pipeline de Machine Learning no terminal:
```bash
python src/ml/treinar_modelo.py
```
*(O script fará a limpeza, o tratamento de dados nulos do INEP, dividirá a base entre treino e teste e salvará o artefato `classificador_escolas.joblib` automaticamente na pasta `models/`).*

### Passo 6: Iniciar o Agente Conversacional
Com o modelo gerado com sucesso, inicie o chat interativo em tempo real:
```bash
python main.py
```
*(O terminal será limpo e o prompt ficará aguardando suas perguntas sobre a infraestrutura das escolas).*

---

### Exemplo Prático de Interação

Graças ao uso do `InMemoryRunner`, o agente mantém o contexto da sessão. Assim que o terminal iniciar, você pode conversar com o agente assim:

> **[Você]:** Olá, gostaria de analisar uma escola. Ela atende 150 alunos, não tem internet nem esgoto, mas possui biblioteca.
> 
> **[Agente]:** Com base nos dados fornecidos, realizei a auditoria e a escola foi classificada com prioridade **Alta** para investimentos de infraestrutura. 
> Justificativa: Apesar de contar com o espaço da biblioteca (1), a unidade atende 150 alunos em situação de vulnerabilidade, operando sem acesso à internet (0) e sem esgoto básico (0). Recomenda-se a alocação imediata de recursos orçamentários para mitigar esses déficits.
