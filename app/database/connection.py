from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

url_original = settings.DATABASE_URL

# Remove possíveis prefixos indesejados
if url_original and url_original.startswith("Value: "):
    url_original = url_original.replace("Value: ", "", 1)
url_original = url_original.strip()

logger.info(f"Conectando ao banco: {url_original[:30]}...")

engine = create_engine(
    url_original,
    echo=True if settings.ENVIRONMENT == "development" else False,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cria as tabelas automaticamente na inicialização
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tabelas criadas/verificadas com sucesso!")
except Exception as e:
    logger.error(f"Erro ao criar tabelas: {e}")
