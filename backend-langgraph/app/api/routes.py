from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.graph.agent import agent

router = APIRouter()

class InvokeRequest(BaseModel):
    question: str

class InvokeResponse(BaseModel):
    generation: str
    router_decision: Optional[str] = None
    is_relevant: Optional[bool] = None

@router.post("/invoke", response_model=InvokeResponse, tags=["Agent"])
async def invoke_agent(request: InvokeRequest):
    try:
        # Invocamos el agente con el estado inicial
        result = agent.invoke({"question": request.question})
        
        return InvokeResponse(
            generation=result.get("generation", ""),
            router_decision=result.get("router_decision"),
            is_relevant=result.get("is_relevant")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
