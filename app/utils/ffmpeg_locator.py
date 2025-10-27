"""
Utilitário para localizar FFmpeg tanto em desenvolvimento quanto no executável compilado
"""
import os
import sys
import shutil
from pathlib import Path

def get_ffmpeg_path() -> str:
    """
    Retorna o caminho correto do FFmpeg baseado no ambiente:
    - No executável PyInstaller: usa o ffmpeg empacotado
    - Em desenvolvimento: usa o ffmpeg do sistema
    """
    # Verificar se está rodando como executável PyInstaller
    if getattr(sys, 'frozen', False):
        # Está rodando como executável
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller cria uma pasta temporária _MEIPASS com os arquivos
            bundle_dir = sys._MEIPASS
        else:
            # Fallback: usar o diretório do executável
            bundle_dir = os.path.dirname(sys.executable)

        # Possíveis nomes no bundle: 'ffmpeg' (Unix) ou 'ffmpeg.exe' (Windows)
        candidates = [
            os.path.join(bundle_dir, 'ffmpeg'),
            os.path.join(bundle_dir, 'ffmpeg.exe'),
            os.path.join(bundle_dir, 'bin', 'ffmpeg'),
            os.path.join(bundle_dir, 'bin', 'ffmpeg.exe'),
        ]

        for ff in candidates:
            if os.path.exists(ff):
                return ff

        # Se não encontrou, retornar 'ffmpeg' para que o sistema tente no PATH
        return 'ffmpeg'
    else:
        # Está rodando em desenvolvimento - usar o ffmpeg do sistema
        # Tentar encontrar no PATH
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            return ffmpeg_path

        # Fallback para locais comuns no macOS
        common_paths = [
            '/opt/homebrew/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/usr/bin/ffmpeg',
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        # Se não encontrou, retornar 'ffmpeg' e deixar o sistema tentar
        return 'ffmpeg'

def get_ffprobe_path() -> str:
    """
    Retorna o caminho correto do FFprobe baseado no ambiente
    """
    ffmpeg_path = get_ffmpeg_path()

    # Se o caminho aponta para um binário com nome completo, trocar pelo ffprobe
    if ffmpeg_path and os.path.basename(ffmpeg_path).lower().startswith('ffmpeg'):
        base = os.path.dirname(ffmpeg_path)
        # Preferir ffprobe.exe em Windows
        candidates = [
            os.path.join(base, 'ffprobe.exe'),
            os.path.join(base, 'ffprobe'),
        ]
        for cand in candidates:
            if os.path.exists(cand):
                return cand

    # Fallback
    return 'ffprobe'

def get_ffmpeg_location_for_ytdlp() -> str:
    """
    Retorna o diretório onde o FFmpeg está localizado (para yt-dlp)
    yt-dlp espera o diretório, não o executável completo
    """
    ffmpeg_path = get_ffmpeg_path()

    if not ffmpeg_path or ffmpeg_path in ('ffmpeg', 'ffmpeg.exe'):
        # Não encontrou caminho específico, retornar None
        # yt-dlp vai procurar no PATH
        return None

    # Retornar apenas o diretório
    return os.path.dirname(ffmpeg_path)

def verify_ffmpeg_available() -> bool:
    """
    Verifica se o FFmpeg está disponível e funcional
    """
    import subprocess

    try:
        ffmpeg_path = get_ffmpeg_path()
        result = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False
