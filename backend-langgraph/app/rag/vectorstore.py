import os
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

def get_retriever():
    """
    Exporta el retriever configurado para recuperar exactamente 7 chunks (k=7)
    usando QdrantCloud y los embeddings especificados.
    """
    # 1. Instancia HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Configuraciones de Qdrant desde variables de entorno
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "institucional")
    
    # 2. Conecta a Qdrant Cloud usando QdrantVectorStore.from_existing_collection
    # O alternativamente inicializando el cliente y pasando al vector store.
    # Aquí usamos from_existing_collection que es un classmethod si usamos langchain_qdrant.
    vectorstore = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=collection_name,
        url=qdrant_url,
        api_key=qdrant_api_key
    )
    
    # 3. Retorna un retriever con k=7
    return vectorstore.as_retriever(search_kwargs={"k": 7})
