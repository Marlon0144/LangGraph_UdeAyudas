from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenRouter API settings
    openrouter_api_key: str
    llm_model: str = "meta-llama/llama-3-8b-instruct:free"
    
    # Qdrant local path settings
    qdrant_path: str = "./local_qdrant"
    qdrant_collection_name: str = "institucional"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
