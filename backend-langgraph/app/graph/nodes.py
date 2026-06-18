from typing import Any, Dict
from app.rag.vectorstore import get_retriever

def retrieve_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nodo de recuperación (retrieve).
    Obtiene los documentos de la base de datos vectorial y formatea el contexto
    estrictamente según los metadatos y la estructura solicitada.
    """
    question = state.get("question", "")
    
    retriever = get_retriever()
    docs = retriever.invoke(question)
    
    context_blocks = []
    
    for doc in docs:
        # Extrae la metadata e inyecta en el f-string con formato estricto
        context_block = f"""--- INICIO DOCUMENTO ---
Fuente: {doc.metadata.get('source_pdf', 'Desconocida')}
Norma: Acuerdo {doc.metadata.get('numero', 'N/A')} del {doc.metadata.get('fecha_expedicion', 'N/A')}
Sección: {doc.metadata.get('section_marker', 'Sin sección específica')}

Contenido:
{doc.page_content}
--- FIN DOCUMENTO ---"""
        context_blocks.append(context_block)
        
    # Guarda este string final concatenado en state["context"]
    state["context"] = "\n\n".join(context_blocks)
    
    return state
