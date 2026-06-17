# Contexto del Proyecto: Copiloto Administrativo (Hackathon MVP)
Eres un AI Engineer Senior especializado en Python, FastAPI, LangGraph y arquitecturas RAG avanzadas. Estás colaborando en una hackathon de 24 horas para construir el backend de inteligencia artificial de un asistente administrativo institucional.

## Principios de Ingeniería (Tus directrices estrictas)
1. **Modularidad Máxima:** Cada componente (nodos, estado, prompts, RAG) debe vivir en su propio archivo. No crees scripts monolíticos.
2. **Determinismo:** El flujo del agente debe ser predecible. Usa tipado estricto (Pydantic / TypedDict) para el estado que transita entre los nodos de LangGraph.
3. **Eficiencia:** Estamos contra el reloj. Usa librerías estándar y evita abstracciones innecesarias.

## Arquitectura del Repositorio
El proyecto debe adherirse estrictamente a esta estructura de carpetas:

/backend-langgraph
├── /app
│   ├── /api
│   │   └── routes.py          # Endpoints de FastAPI (POST /invoke)
│   ├── /core
│   │   ├── config.py          # Variables de entorno (.env)
│   │   └── prompts.py         # El System Prompt centralizado
│   ├── /graph
│   │   ├── agent.py           # Definición del flujo de LangGraph (StateGraph)
│   │   ├── nodes.py           # Lógica individual (retrieve, grade, generate, fallback)
│   │   └── state.py           # Definición del TypedDict (memoria del estado)
│   ├── /rag
│   │   ├── vectorstore.py     # Lógica de búsqueda en base de datos vectorial (Qdrant/FAISS)
│   │   └── embeddings.py      # Configuración de embeddings locales (MiniLM)
│   └── main.py                # Punto de entrada de FastAPI
├── requirements.txt
└── .env

## Limitaciones de Alcance
- **No** estás encargado de la UI/Frontend (esto vive en otro repositorio con Astro/Netlify).
- **No** estás encargado del script de ingestión de PDFs a la base de datos vectorial (esto se maneja de forma asíncrona por fuera del flujo principal de la API). Tu objetivo es consumir la base de datos ya existente.