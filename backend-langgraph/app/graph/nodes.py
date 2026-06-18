from typing import Dict, Any
from app.graph.state import AgentState
from app.core.prompts import QA_MASTER_PROMPT, GRADER_PROMPT, ROUTER_PROMPT
from app.core.config import settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Inicializamos el LLM de OpenRouter usando la compatibilidad con OpenAI
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
    model=settings.llm_model,
)

def route_question(state: AgentState) -> Dict[str, Any]:
    """
    Nodo que evalúa si la pregunta es ADMINISTRATIVA o CASUAL.
    """
    print("---ROUTE QUESTION---")
    question = state["question"]
    
    prompt = PromptTemplate(template=ROUTER_PROMPT, input_variables=["question"])
    chain = prompt | llm | StrOutputParser()
    
    decision = chain.invoke({"question": question})
    decision = decision.strip().upper()
    if "ADMINISTRATIVA" in decision:
        decision = "ADMINISTRATIVA"
    elif "CASUAL" in decision:
        decision = "CASUAL"
    else:
        decision = "ADMINISTRATIVA"  # fallback
        
    return {"router_decision": decision}

def retrieve(state: AgentState) -> Dict[str, Any]:
    """
    Nodo que recupera documentos de la base de datos vectorial basados en la pregunta.
    """
    print("---RETRIEVE---")
    question = state["question"]
    
    documents = ["(Documento simulado) El horario de atención en la secretaría académica es de 8:00 AM a 5:00 PM de lunes a viernes."]
    
    return {"context": documents}

def grade_documents(state: AgentState) -> Dict[str, Any]:
    """
    Nodo que evalúa si los documentos recuperados son relevantes para la pregunta usando el LLM.
    """
    print("---GRADE DOCUMENTS---")
    question = state["question"]
    documents = state.get("context", [])
    
    if not documents:
        return {"is_relevant": False, "context": []}
        
    context_str = "\n".join(documents)
    prompt = PromptTemplate(template=GRADER_PROMPT, input_variables=["question", "context"])
    chain = prompt | llm | StrOutputParser()
    
    # Evaluate using LLM
    score = chain.invoke({"question": question, "context": context_str})
    is_relevant = "yes" in score.strip().lower()
    
    return {"is_relevant": is_relevant, "context": documents}

def generate(state: AgentState) -> Dict[str, Any]:
    """
    Nodo que genera una respuesta utilizando los documentos relevantes.
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["context"]
    
    context_str = "\n".join(documents)
    prompt = PromptTemplate(template=QA_MASTER_PROMPT, input_variables=["question", "context"])
    chain = prompt | llm | StrOutputParser()
    
    generation = chain.invoke({"question": question, "context": context_str})
    
    return {"generation": generation}

def direct_answer(state: AgentState) -> Dict[str, Any]:
    """
    Nodo que responde cortésmente a preguntas casuales.
    """
    print("---DIRECT ANSWER---")
    question = state["question"]
    
    prompt = PromptTemplate.from_template("You are a friendly institutional assistant. Briefly respond to this casual message in a friendly way. Message: {question}")
    chain = prompt | llm | StrOutputParser()
    
    generation = chain.invoke({"question": question})
    
    return {"generation": generation}

def fallback(state: AgentState) -> Dict[str, Any]:
    """
    Nodo de fallback cuando no hay documentos relevantes.
    """
    print("---FALLBACK---")
    return {"generation": "Lo siento, no pude encontrar información institucional sobre eso."}
