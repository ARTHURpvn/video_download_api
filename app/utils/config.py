import os
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Diretório Downloads do usuário
def get_user_downloads_dir():
    """Obtém o diretório Downloads do usuário"""
    home = Path.home()
    downloads_dir = home / "Downloads" / "luiz_da_o_butico"
    downloads_dir.mkdir(exist_ok=True)
    return str(downloads_dir)

DOWNLOAD_DIR = get_user_downloads_dir()

# Configurações do CORS
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# Configurações da API
API_TITLE = "YouTube Video Downloader API"
API_VERSION = "1.0.0"
