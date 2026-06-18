from typing import Any, Dict
from langchain_openai import ChatOpenAI
from app.rag.vectorstore import get_retriever
from app.core.config import settings
from app.core.prompts import QA_MASTER_PROMPT

def route_question_node(state: Dict[str, Any]) -> Dict[str, Any]:
    question = state.get("question", "")
    if "hola" in question.lower() or "buenos días" in question.lower():
        state["router_decision"] = "CASUAL"
    else:
        state["router_decision"] = "ADMINISTRATIVA"
    return state

def retrieve_node(state: Dict[str, Any]) -> Dict[str, Any]:
    question = state.get("question", "")
    retriever = get_retriever()
    docs = retriever.invoke(question)
    context_blocks = []
    for doc in docs:
        context_block = f"""--- INICIO DOCUMENTO ---
Fuente: {doc.metadata.get('source_pdf', 'Desconocida')}
Norma: Acuerdo {doc.metadata.get('numero', 'N/A')} del {doc.metadata.get('fecha_expedicion', 'N/A')}
Sección: {doc.metadata.get('section_marker', 'Sin sección específica')}

Contenido:
{doc.page_content}
--- FIN DOCUMENTO ---"""
        context_blocks.append(context_block)
    state["context"] = "\n\n".join(context_blocks)
    return state

def grade_documents_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["is_relevant"] = True
    return state

def generate_node(state: Dict[str, Any]) -> Dict[str, Any]:
    question = state.get("question", "")
    context = state.get("context", "")
    prompt = QA_MASTER_PROMPT.format(context=context, question=question)
    try:
        llm = ChatOpenAI(
            model="openai/gpt-4o-mini",
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        response = llm.invoke(prompt)
        state["generation"] = response.content
    except Exception as e:
        print(f"[ERROR generate_node] Fallo al invocar el LLM: {e}")
        state["generation"] = "Lo siento, ocurrió un error al generar la respuesta."
    return state

def direct_answer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    question = state.get("question", "")
    try:
        llm = ChatOpenAI(
            model="openai/gpt-4o-mini",
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        prompt = f"Responde de forma amigable y breve al siguiente saludo: {question}"
        response = llm.invoke(prompt)
        state["generation"] = response.content
    except Exception as e:
        print(f"[ERROR direct_answer_node] Fallo al invocar el LLM: {e}")
        state["generation"] = "¡Hola! Soy el asistente administrativo institucional. ¿En qué puedo ayudarte?"
    return state

def fallback_node(state: Dict[str, Any]) -> Dict[str, Any]:
    state["generation"] = "No encontré información relevante en los documentos institucionales para responder tu pregunta. Por favor, intenta reformularla o contacta a la oficina correspondiente."
    return state
