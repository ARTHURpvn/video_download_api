import re
import logging
import os
from ..utils.config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)

def normalize_youtube_url(url: str) -> str:
    """Normaliza URLs do YouTube para formato padrão"""
    # Remover parâmetros desnecessários e normalizar
    video_id_patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/.*[?&]v=([a-zA-Z0-9_-]{11})'
    ]

    for pattern in video_id_patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            if '/shorts/' in url.lower():
                return f"https://www.youtube.com/shorts/{video_id}"
            else:
                return f"https://www.youtube.com/watch?v={video_id}"

    return url

def is_youtube_short(url: str) -> bool:
    """Verifica se a URL é de um YouTube Short"""
    return '/shorts/' in url.lower() or 'youtube.com/shorts' in url.lower()

def sanitize_filename(title: str) -> str:
    """Limpa caracteres especiais do título para nome de arquivo"""
    return "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

def get_next_video_number() -> int:
    """Obtém o próximo número sequencial para nomear o vídeo"""
    try:
        if not os.path.exists(DOWNLOAD_DIR):
            return 1

        # Listar todos os arquivos que começam com "video_"
        existing_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith('video_')]

        if not existing_files:
            return 1

        # Extrair números dos arquivos existentes
        numbers = []
        for file in existing_files:
            # Procurar padrão video_X.extensão
            match = re.match(r'video_(\d+)\.\w+', file)
            if match:
                numbers.append(int(match.group(1)))

        if not numbers:
            return 1

        # Retornar o próximo número
        return max(numbers) + 1

    except Exception as e:
        logger.warning(f"Erro ao obter número do vídeo: {e}")
        return 1

def generate_video_filename(extension: str = "mp4") -> str:
    """Gera o nome do arquivo no formato video_X.extensão"""
    video_number = get_next_video_number()
    return f"video_{video_number}.{extension}"
