from fastapi import APIRouter
import os
import subprocess
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["health"])

@router.get("/")
async def root():
    return {
        "message": "YouTube Video Downloader API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@router.get("/health")
async def health_check():
    """Endpoint de health check para verificar se a API está funcionando"""
    try:
        # Verificar yt-dlp
        yt_dlp_version = "unknown"
        try:
            result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=5)
            yt_dlp_version = result.stdout.strip() if result.returncode == 0 else "error"
        except:
            yt_dlp_version = "not installed"

        # Verificar ffmpeg
        ffmpeg_available = False
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
            ffmpeg_available = result.returncode == 0
        except:
            ffmpeg_available = False

        # Verificar diretório de downloads
        from ..utils.config import DOWNLOAD_DIR
        downloads_dir_exists = os.path.exists(DOWNLOAD_DIR)
        downloads_dir_writable = os.access(DOWNLOAD_DIR, os.W_OK) if downloads_dir_exists else False

        # Status geral
        all_healthy = ffmpeg_available and downloads_dir_writable and yt_dlp_version != "not installed"

        return {
            "status": "healthy" if all_healthy else "degraded",
            "message": "API está funcionando" if all_healthy else "API funcionando com limitações",
            "checks": {
                "yt_dlp": {
                    "available": yt_dlp_version != "not installed",
                    "version": yt_dlp_version
                },
                "ffmpeg": {
                    "available": ffmpeg_available
                },
                "storage": {
                    "downloads_dir": DOWNLOAD_DIR,
                    "exists": downloads_dir_exists,
                    "writable": downloads_dir_writable
                }
            },
            "environment": {
                "is_render": os.environ.get('RENDER') == 'true',
                "port": os.environ.get('PORT', '8000')
            }
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "unhealthy",
            "message": f"Error: {str(e)}"
        }

@router.options("/video/info")
@router.options("/video/download")
@router.options("/video/download-stream")
@router.options("/downloads")
@router.options("/downloads/{filename}")
async def options_handler():
    """Manipula requisições OPTIONS para CORS"""
    return {"message": "OK"}

@router.get("/debug/common-errors")
async def list_common_errors():
    """Lista os principais erros 400 e suas possíveis soluções"""
    return {
        "common_400_errors": {
            "1. Video unavailable": {
                "causes": [
                    "Vídeo privado ou removido",
                    "Vídeo com restrição de idade",
                    "Vídeo com restrição geográfica",
                    "URL inválida ou malformada"
                ],
                "solutions": [
                    "Verificar se o vídeo existe no YouTube",
                    "Tentar com URL diferente (youtu.be vs youtube.com)",
                    "Usar VPN se for restrição geográfica"
                ]
            },
            "2. Sign in to confirm your age": {
                "causes": [
                    "Vídeo com restrição de idade",
                    "YouTube requer login"
                ],
                "solutions": [
                    "Usar configurações diferentes no yt-dlp",
                    "Tentar com cliente Android/iOS"
                ]
            },
            "3. HTTP Error 403: Forbidden": {
                "causes": [
                    "YouTube detectou bot/automação",
                    "Rate limiting",
                    "Headers HTTP inadequados"
                ],
                "solutions": [
                    "Usar user-agent realista",
                    "Adicionar delays entre requisições",
                    "Usar diferentes player clients (Android, iOS)"
                ]
            },
            "4. Extraction failed": {
                "causes": [
                    "Mudanças na API do YouTube",
                    "yt-dlp desatualizado",
                    "Formato não disponível"
                ],
                "solutions": [
                    "Atualizar yt-dlp",
                    "Tentar formatos diferentes",
                    "Usar fallback strategies"
                ]
            },
            "5. This live event has ended": {
                "causes": [
                    "Tentativa de baixar live stream que acabou",
                    "Vídeo ainda sendo processado"
                ],
                "solutions": [
                    "Aguardar processamento completo",
                    "Tentar novamente mais tarde"
                ]
            }
        },
        "troubleshooting_steps": [
            "1. Testar URL no navegador primeiro",
            "2. Verificar se é URL válida do YouTube",
            "3. Tentar com /video/diagnose endpoint",
            "4. Verificar logs do servidor",
            "5. Testar com vídeos públicos simples primeiro"
        ]
    }
