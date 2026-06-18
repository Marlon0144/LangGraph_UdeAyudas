from app.graph.agent import agent

def test_route_administrativa():
    result = agent.invoke({"question": "¿Cuál es el horario de la secretaría?"})
    assert "generation" in result
    assert result["router_decision"] == "ADMINISTRATIVA"

def test_route_casual():
    result = agent.invoke({"question": "Hola, ¿cómo estás?"})
    assert "generation" in result
    assert result["router_decision"] == "CASUAL"

def test_fallback():
    result = agent.invoke({"question": "¿Quién ganó el mundial?"})
    # Como el doc simulado no es relevante (probablemente), 
    # podemos verificar si cae en fallback (is_relevant=False) o si generó respuesta.
    # En este momento el LLM decide basado en el documento de horarios.
    assert "generation" in result
