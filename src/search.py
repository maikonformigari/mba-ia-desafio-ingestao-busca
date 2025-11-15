import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    # Validando a pergunta
    if not question or not question.strip():
        raise ValueError("A pergunta não pode estar vazia. Por favor, insira uma pergunta.")
    
    ## Criando modelo de embeddings
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    ## Conectando ao banco de dados
    db = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )    

    ## Realizando a busca vetorial por similaridade
    results = db.similarity_search_with_score(question, k=10)

    # Criando o contexto a partir dos resultados da busca
    contexto = "\n".join([doc.page_content for doc, _ in results])

    # Criando o prompt template
    promptTemplate = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )                

    # Criando o modelo
    model = ChatOpenAI(model="gpt-5-nano", temperature=0.5)

    # Criando chain com o prompt e o modelo
    chain = promptTemplate | model

    # Executando chain
    result = chain.invoke({"contexto": contexto, "pergunta": question})
    return result.content

    