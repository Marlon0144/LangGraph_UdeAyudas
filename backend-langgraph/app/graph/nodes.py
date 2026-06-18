from typing import Any, Dict
from app.rag.vectorstore import get_retriever

def route_question_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nodo de enrutamiento inicial.
    Define hacia dónde debe ir la pregunta inicialmente.
    """
    question = state.get("question", "")
    # Lógica básica para ejemplificar el ruteo
    if "hola" in question.lower() or "buenos días" in question.lower():
        state["router_decision"] = "CASUAL"
    else:
        state["router_decision"] = "ADMINISTRATIVA"
    return state

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

def grade_documents_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evalúa si los documentos recuperados son relevantes para la pregunta.
    """
    # Lógica dummy
    state["is_relevant"] = True
    return state

def generate_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera la respuesta usando el contexto recuperado.
    """
    return state

def direct_answer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Responde directamente a preguntas casuales.
    """
    return state

def fallback_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Respuesta por defecto cuando no se encuentra información.
    """
    return state
