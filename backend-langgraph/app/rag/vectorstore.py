import os
from app.core.config import settings
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings

def get_retriever():
    """
    Exporta el retriever configurado para recuperar exactamente 7 chunks (k=7)
    usando QdrantCloud y los embeddings en la nube de Hugging Face (cero consumo de RAM local).
    """
    # 1. Instancia los embeddings apuntando a la API gratuita de Hugging Face
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        huggingfacehub_api_token=os.getenv("HF_TOKEN")
    )

    # 2. Conecta a Qdrant Cloud usando QdrantVectorStore.from_existing_collection
    vectorstore = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name="udea_reglamento_pregrado",
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )

    # 3. Retorna un retriever con k=7
    return vectorstore.as_retriever(search_kwargs={"k": 7})