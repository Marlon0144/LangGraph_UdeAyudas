from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import route_question, retrieve, grade_documents, generate, direct_answer, fallback

def route_initial(state: AgentState) -> str:
    """
    Enruta inicialmente la pregunta según si es administrativa o casual.
    """
    print("---ROUTE INITIAL---")
    decision = state.get("router_decision", "ADMINISTRATIVA")
    if decision == "CASUAL":
        return "direct_answer"
    else:
        return "retrieve"

def decide_to_generate(state: AgentState) -> str:
    """
    Determina el siguiente nodo basándose en la relevancia de los documentos.
    """
    print("---DECIDE TO GENERATE---")
    if state.get("is_relevant"):
        return "generate"
    else:
        return "fallback"

# Definir el grafo
workflow = StateGraph(AgentState)

# Añadir nodos
workflow.add_node("route_question", route_question)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("direct_answer", direct_answer)
workflow.add_node("fallback", fallback)

# Definir aristas
workflow.set_entry_point("route_question")

# Arista condicional de enrutamiento inicial
workflow.add_conditional_edges(
    "route_question",
    route_initial,
    {
        "retrieve": "retrieve",
        "direct_answer": "direct_answer"
    }
)

workflow.add_edge("retrieve", "grade_documents")

# Arista condicional de generación
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "generate": "generate",
        "fallback": "fallback"
    }
)

workflow.add_edge("generate", END)
workflow.add_edge("direct_answer", END)
workflow.add_edge("fallback", END)

# Compilar
agent = workflow.compile()
