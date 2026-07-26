from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DATABASE_URL: str
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    GEMINI_MODEL: str = "gemini-2.0-flash"  # ← ATUALIZADO!
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2048
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

if not settings.DATABASE_URL:
    logger.error("❌ DATABASE_URL não encontrada!")
else:
    logger.info(f"✅ DATABASE_URL carregada ({len(settings.DATABASE_URL)} caracteres)")
