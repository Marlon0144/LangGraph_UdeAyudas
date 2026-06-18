from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.graph.agent import agent

router = APIRouter()

class InvokeRequest(BaseModel):
    question: str
    debug_mode: bool = False

class InvokeResponse(BaseModel):
    generation: str
    router_decision: Optional[str] = None
    is_relevant: Optional[bool] = None
    context: Optional[str] = None

@router.post("/invoke", response_model=InvokeResponse, tags=["Agent"])
async def invoke_agent(request: InvokeRequest):
    try:
        # Invocamos el agente con el estado inicial
        result = agent.invoke({
            "question": request.question,
            "context": "",
            "generation": "",
            "is_relevant": False,
            "router_decision": ""
        })
        
        generation = result.get("generation", "")
        context = result.get("context", "")
        
        # Lógica de intercepción basada en debug_mode
        if request.debug_mode and context:
            generation = f"**--- CONTEXTO RECUPERADO (MODO DEBUG) ---**\n\n{context}\n\n**--- RESPUESTA DEL ASISTENTE ---**\n\n{generation}"
        
        return InvokeResponse(
            generation=generation,
            router_decision=result.get("router_decision"),
            is_relevant=result.get("is_relevant"),
            context=context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
