from app.core.config import settings
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

    # 2. Conecta a Qdrant Cloud usando QdrantVectorStore.from_existing_collection
    vectorstore = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=settings.qdrant_collection_name,
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )

    # 3. Retorna un retriever con k=7
    return vectorstore.as_retriever(search_kwargs={"k": 7})
