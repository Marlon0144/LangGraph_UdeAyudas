# Copiloto Administrativo

Backend de inteligencia artificial para un asistente administrativo institucional, construido con **LangGraph** + **FastAPI** + **OpenRouter**.

## Arquitectura

El proyecto sigue una arquitectura modular basada en un grafo de agentes con LangGraph:

```
backend-langgraph/
├── app/
│   ├── api/
│   │   └── routes.py        # Endpoint POST /api/invoke
│   ├── core/
│   │   ├── config.py        # Variables de entorno (Pydantic Settings)
│   │   └── prompts.py       # System prompts del agente
│   ├── graph/
│   │   ├── agent.py         # Definición del grafo (StateGraph)
│   │   ├── nodes.py         # Nodos del grafo (route_question, retrieve, grade, generate, fallback)
│   │   └── state.py         # Tipado del estado (TypedDict)
│   ├── rag/
│   │   ├── embeddings.py    # Configuración de embeddings (MiniLM)
│   │   └── vectorstore.py   # Búsqueda en base vectorial (Qdrant)
│   └── main.py              # Punto de entrada de FastAPI
├── tests/
│   ├── test_agent.py        # Tests unitarios del grafo
│   └── test_api.py          # Tests E2E de la API
└── requirements.txt
```

### Flujo del agente

```
Pregunta → route_question → [ADMINISTRATIVA → retrieve → grade_documents → (generate | fallback)]
                           [CASUAL → direct_answer]
```

## Configuración local

Sigue estos pasos para clonar y ejecutar el proyecto en local.

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd LangGraph_UdeAyudas
```

### 2. Configurar el archivo .env

Copia el archivo de ejemplo y completa la API Key de OpenRouter:

```bash
copy .env.example .env
```

Edita `.env` para que tenga el siguiente contenido:

```env
OPENROUTER_API_KEY=sk-or-v1-tu-api-key-aqui
LLM_MODEL=meta-llama/llama-3-8b-instruct
```

> **Importante:** Este `.env` debe existir también dentro de `backend-langgraph/`. Cópialo:
> ```bash
> copy .env backend-langgraph\.env
> ```

### 3. Crear y activar entorno virtual (recomendado)

```bash
# Crear el entorno virtual
python -m venv venv

# Activar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si da error de permisos, ejecuta antes:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 4. Instalar dependencias

```bash
pip install -r backend-langgraph/requirements.txt
```

### 5. Levantar la API

```bash
cd backend-langgraph
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

### 6. Probar el endpoint

```bash
curl -X POST http://localhost:8000/api/invoke \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"¿Cuál es el horario de secretaría?\"}"
```

También puedes abrir en el navegador:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Tests

```bash
cd backend-langgraph
python -m pytest tests/ -v
```
