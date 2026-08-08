from pathlib import Path
from pydantic_settings import BaseSettings

# Project root is 2 levels up from this file (backend/app/core/ -> backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model_name: str = "gemma-finetuned:4-bit"
    gguf_path: str = "backend/ml_assets/gemma/model.gguf"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_origin: str = "http://localhost:3000"

    retrieval_top_k: int = 5
    rag_backend: str = "FAISS"

    demo_mode: bool = True
    demo_cache_path: str = "demo-assets/cached_responses.json"

    ml_assets_dir: str = str(PROJECT_ROOT / "ml_assets")

    # Gemini (safety/router agent). Keys are read from the repo-root .env as
    # GEMINI_API_KEY_1..N and rotated round-robin with a per-key cooldown.
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_key_cooldown_seconds: float = 6.0
    env_file_path: str = str(PROJECT_ROOT.parent / ".env")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
