from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router

app = FastAPI(
    title="Copiloto Administrativo API",
    description="Backend LangGraph + FastAPI para el asistente institucional.",
    version="1.0.0"
)

# Configuración de CORS para permitir la comunicación con el frontend de Astro/Netlify
# ⚠️  EN PRODUCCIÓN: Reemplazar "http://localhost:4321" por la URL real de Netlify (ej. "https://tudominio.netlify.app")
# para proteger la API contra orígenes no autorizados.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
