from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .utils.config import (
    API_TITLE,
    API_VERSION,
    API_DESCRIPTION,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS
)
from .routes import video, downloads, health

# Configurar logging para produção
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Incluir rotas
app.include_router(health.router)
app.include_router(video.router)
app.include_router(downloads.router)

@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação"""
    logger.info("🚀 Iniciando YouTube Downloader API...")
    logger.info(f"📦 Versão: {API_VERSION}")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado ao encerrar a aplicação"""
    logger.info("👋 Encerrando YouTube Downloader API...")
