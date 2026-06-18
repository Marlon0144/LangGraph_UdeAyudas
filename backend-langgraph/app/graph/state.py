from typing import TypedDict

class AgentState(TypedDict):
    """
    Representa el estado del agente de LangGraph que fluye entre los nodos.
    """
    question: str
    context: str
    generation: str
    is_relevant: bool
    router_decision: str
