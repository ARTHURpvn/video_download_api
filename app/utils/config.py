import os
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Diretório de downloads - adaptado para produção (Render)
def get_downloads_dir():
    """Obtém o diretório de downloads - funciona em dev e produção"""
    # Em produção (Render), usar /tmp que é o único diretório gravável
    if os.environ.get('RENDER'):
        downloads_dir = Path('/tmp/videos')
    else:
        # Em desenvolvimento, usar Downloads do usuário
        home = Path.home()
        downloads_dir = home / "Downloads" / "luiz_da_o_butico"

    downloads_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Diretório de downloads: {downloads_dir}")
    return str(downloads_dir)

DOWNLOAD_DIR = get_downloads_dir()

# Configurações do CORS - permitir frontend
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://*.vercel.app",
    "https://*.netlify.app",
    "https://*.render.com",
    "*"  # Para desenvolvimento - remover em produção se necessário
]
CORS_CREDENTIALS = True
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# Configurações da API
API_TITLE = "YouTube Video Downloader API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para download de vídeos do YouTube com suporte a streaming em tempo real"

# Porta para o servidor (Render usa a variável PORT)
PORT = int(os.environ.get('PORT', 8000))
HOST = os.environ.get('HOST', '0.0.0.0')
