import yt_dlp
import logging
import asyncio
from typing import Dict
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json

from ..models.schemas import VideoRequest, VideoInfo, DownloadResponse, DiagnosisResponse, DownloadProgress
from ..services.youtube import get_video_info_robust, download_video_robust
from ..services.file_manager import find_downloaded_file, get_file_path
from ..utils.helpers import normalize_youtube_url, is_youtube_short

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/video", tags=["video"])

# Armazenar progresso por sessão/ID
download_progress_store: Dict[str, DownloadProgress] = {}

@router.post("/info", response_model=VideoInfo)
async def get_video_information(request: VideoRequest):
    """Obtém informações do vídeo sem baixar"""
    try:
        info = get_video_info_robust(str(request.url))

        # Extrair thumbnail - YouTube fornece várias opções, pegar a melhor
        thumbnail_url = None
        if 'thumbnails' in info and info['thumbnails']:
            # Pegar a thumbnail de melhor qualidade (última da lista)
            thumbnail_url = info['thumbnails'][-1]['url']
        elif 'thumbnail' in info:
            thumbnail_url = info['thumbnail']

        return VideoInfo(
            title=info.get('title', 'N/A'),
            duration=info.get('duration'),
            uploader=info.get('uploader', 'N/A'),
            view_count=info.get('view_count'),
            upload_date=info.get('upload_date'),
            description=info.get('description', '')[:500] if info.get('description') else None,
            thumbnail=thumbnail_url
        )
    except Exception as e:
        logger.error(f"Erro ao obter informações do vídeo: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/download", response_model=DownloadResponse)
async def download_video(request: VideoRequest):
    """Baixa o vídeo do YouTube (incluindo Shorts) - Versão robusta anti-403"""
    try:
        # Usar a nova função robusta de download
        info = download_video_robust(str(request.url), request)

        # Verificar se é um YouTube Short
        is_short = is_youtube_short(str(request.url))

        title = info.get('title', 'video')
        downloaded_file = find_downloaded_file(title)

        # Extrair thumbnail - YouTube fornece várias opções, pegar a melhor
        thumbnail_url = None
        if 'thumbnails' in info and info['thumbnails']:
            # Pegar a thumbnail de melhor qualidade (última da lista)
            thumbnail_url = info['thumbnails'][-1]['url']
        elif 'thumbnail' in info:
            thumbnail_url = info['thumbnail']

        video_info = VideoInfo(
            title=info.get('title', 'N/A'),
            duration=info.get('duration'),
            uploader=info.get('uploader', 'N/A'),
            view_count=info.get('view_count'),
            upload_date=info.get('upload_date'),
            description=info.get('description', '')[:500] if info.get('description') else None,
            thumbnail=thumbnail_url
        )

        video_type = "Short" if is_short else "vídeo"

        return DownloadResponse(
            status="success",
            message=f"{video_type} baixado com sucesso!",
            filename=downloaded_file,
            file_path=get_file_path(downloaded_file) if downloaded_file else None,
            video_info=video_info
        )

    except Exception as e:
        logger.error(f"Erro no download: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erro ao baixar vídeo: {str(e)}")

@router.post("/download-stream")
async def download_video_stream(request: VideoRequest):
    """Baixa o vídeo com progresso em tempo real via Server-Sent Events (SSE)"""

    async def event_generator():
        """Gerador de eventos SSE para progresso do download"""

        # Usar uma lista compartilhada para progresso em tempo real
        import threading
        progress_queue = []
        progress_lock = threading.Lock()
        download_complete = threading.Event()

        def progress_callback(progress: DownloadProgress):
            """Callback para receber atualizações de progresso"""
            with progress_lock:
                progress_queue.append(progress)

        try:
            # Enviar evento inicial
            initial_data = {
                'status': 'starting',
                'message': 'Iniciando download...',
                'progress_percent': 0.0
            }
            yield f"data: {json.dumps(initial_data)}\n\n"
            await asyncio.sleep(0.1)

            # Executar download em thread separada
            loop = asyncio.get_event_loop()

            # Iniciar download em background
            download_task = loop.run_in_executor(
                None,
                lambda: download_video_robust(str(request.url), request, progress_callback)
            )

            # Enviar atualizações em tempo real conforme chegam
            last_sent_index = 0

            while not download_task.done():
                # Verificar se há novos progressos para enviar
                with progress_lock:
                    if len(progress_queue) > last_sent_index:
                        # Enviar apenas os novos progressos (não enviados ainda)
                        for i in range(last_sent_index, len(progress_queue)):
                            progress = progress_queue[i]
                            yield f"data: {progress.model_dump_json()}\n\n"
                        last_sent_index = len(progress_queue)

                await asyncio.sleep(0.1)  # Verificar a cada 100ms

            # Aguardar conclusão do download
            info = await download_task

            # Enviar últimos progressos que podem ter chegado após o loop
            with progress_lock:
                if len(progress_queue) > last_sent_index:
                    for i in range(last_sent_index, len(progress_queue)):
                        progress = progress_queue[i]
                        yield f"data: {progress.model_dump_json()}\n\n"

            # Obter informações finais do arquivo
            is_short = is_youtube_short(str(request.url))
            title = info.get('title', 'video')
            downloaded_file = find_downloaded_file(title)

            # Extrair thumbnail
            thumbnail_url = None
            if 'thumbnails' in info and info['thumbnails']:
                thumbnail_url = info['thumbnails'][-1]['url']
            elif 'thumbnail' in info:
                thumbnail_url = info['thumbnail']

            video_info = {
                'title': info.get('title', 'N/A'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader', 'N/A'),
                'view_count': info.get('view_count'),
                'upload_date': info.get('upload_date'),
                'description': info.get('description', '')[:500] if info.get('description') else None,
                'thumbnail': thumbnail_url
            }

            # Enviar evento final de sucesso
            final_response = {
                'status': 'completed',
                'message': f"{'Short' if is_short else 'Vídeo'} baixado com sucesso!",
                'filename': downloaded_file,
                'file_path': get_file_path(downloaded_file) if downloaded_file else None,
                'video_info': video_info,
                'progress_percent': 100.0
            }

            yield f"data: {json.dumps(final_response)}\n\n"

        except Exception as e:
            logger.error(f"Erro no download stream: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

            error_response = {
                'status': 'error',
                'message': f'Erro ao baixar vídeo: {str(e)}',
                'progress_percent': 0.0
            }
            yield f"data: {json.dumps(error_response)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_video_url(request: VideoRequest):
    """Diagnóstica problemas com URLs do YouTube e fornece informações detalhadas"""
    url = str(request.url)
    diagnosis = DiagnosisResponse(
        original_url=url,
        normalized_url=normalize_youtube_url(url),
        is_short=is_youtube_short(url),
        errors=[],
        successful_strategy=None,
        yt_dlp_version=yt_dlp.version.__version__ if hasattr(yt_dlp, 'version') else "unknown"
    )

    try:
        info = get_video_info_robust(url)
        diagnosis.successful_strategy = "robust_extraction"
        diagnosis.video_available = True
        diagnosis.title = info.get('title', 'N/A')
        diagnosis.duration = info.get('duration')
        diagnosis.formats_available = len(info.get('formats', []))
    except Exception as e:
        diagnosis.video_available = False
        diagnosis.errors.append(str(e))

    return diagnosis
