import os
import logging
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
load_dotenv()

# Criando e configurando logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ingest_pdf() -> bool:
    """
    Processa e ingere um arquivo PDF no banco de dados PGVector.
    
    Returns:
        bool: True se o processamento foi bem-sucedido, False caso contrário
    """
    
    # 1. Carregando o arquivo PDF
    try:
        pdf_path = os.getenv("PDF_PATH")
        if not pdf_path or not os.path.exists(pdf_path):
            logger.error(f"Arquivo PDF não encontrado: {pdf_path}")
            return False
            
        logger.info(f"Carregando PDF: {pdf_path}")
        docs = PyPDFLoader(pdf_path).load()
        logger.info(f"PDF carregado com sucesso. Total de páginas: {len(docs)}")        
    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar o PDF: {e}", exc_info=True)
        return False
    
    # 2. Criando os chunks do documento
    try:
        logger.info("Iniciando criação dos chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            add_start_index=False
        )
        chunks = text_splitter.split_documents(docs)
        logger.info(f"Documento dividido em {len(chunks)} chunks")        
    except Exception as e:
        logger.error(f"Erro ao criar os chunks do documento: {e}", exc_info=True)
        return False
    
    # 3. Enriquecendo os metadados dos chunks
    try:
        logger.info("Enriquecendo metadados dos chunks...")
        chunks = enrich_metadata(chunks)
    except Exception as e:
        logger.error(f"Erro ao enriquecer os metadados dos chunks: {e}", exc_info=True)
        return False
    
    # 4. Criando embeddings e armazenando no banco
    try:
        embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        logger.info("Conectando ao banco de dados e armazenando chunks...")
        db = PGVector(
            embeddings=embeddings,
            collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )
        
        db.add_documents(documents=chunks)
        logger.info(f"✅ {len(chunks)} chunks armazenados com sucesso no banco de dados")
        return True
    except ValueError as e:
        logger.error(f"Erro de configuração (verifique variáveis de ambiente): {e}")
        return False
    except Exception as e:
        logger.error(f"Erro ao armazenar os chunks no banco de dados: {e}", exc_info=True)
        return False


def enrich_metadata(chunks: List[Document]) -> List[Document]:
    """
    Enriquece os metadados dos chunks com informações da página.
    
    Args:
        chunks: Lista de documentos a serem enriquecidos
        
    Returns:
        Lista de documentos com metadados enriquecidos
    """
    for chunk in chunks:
        page_number = chunk.metadata.get('page', chunk.metadata.get('page_number', 'unknown'))
        chunk.metadata["source"] = f"page_{page_number}"
    
    return chunks


if __name__ == "__main__":
    success = ingest_pdf()
    exit(0 if success else 1)