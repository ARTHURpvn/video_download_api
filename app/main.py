from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.config import (
    API_TITLE,
    API_VERSION,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS
)
from .routes import video, downloads, health

# Criar aplicação FastAPI
app = FastAPI(title=API_TITLE, version=API_VERSION)

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
