import yt_dlp
import os
import logging
from typing import Dict, Any, Callable, Optional
from fastapi import HTTPException

from ..utils.helpers import normalize_youtube_url, is_youtube_short
from ..utils.config import DOWNLOAD_DIR
from ..models.schemas import VideoRequest, DownloadProgress
from .video_converter import find_and_convert_latest_video

logger = logging.getLogger(__name__)

class DownloadProgressTracker:
    """Classe para rastrear o progresso do download"""
    def __init__(self, callback: Optional[Callable[[DownloadProgress], None]] = None):
        self.callback = callback
        self.current_strategy = None
        self.last_progress = None
        self.max_percent_reached = 0.0  # Track maximum progress reached
        self.strategy_attempts = 0

    def set_strategy(self, strategy_name: str):
        self.current_strategy = strategy_name
        self.strategy_attempts += 1

        # Only send "starting" message if this is the first strategy
        # Otherwise, keep the existing progress
        if self.callback and self.strategy_attempts == 1:
            self.callback(DownloadProgress(
                status='starting',
                current_strategy=strategy_name,
                message=f'Iniciando download com: {strategy_name}',
                progress_percent=0.0
            ))

    def progress_hook(self, d: dict):
        """Hook chamado pelo yt-dlp durante o download"""
        try:
            status = d.get('status')

            if status == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)

                # Calcular percentual
                percent = 0.0
                if total > 0:
                    percent = (downloaded / total) * 100

                # IMPORTANTE: Garantir que o progresso nunca diminua
                # Mapear progresso de estratégias subsequentes para continuar do último máximo
                if percent > 0:
                    # Se estamos em uma nova estratégia (depois de falhas anteriores),
                    # mapear o progresso para continuar de onde paramos
                    if self.strategy_attempts > 1:
                        # Dividir o progresso restante entre as estratégias
                        remaining_progress = 100.0 - self.max_percent_reached
                        adjusted_percent = self.max_percent_reached + (percent * remaining_progress / 100.0)
                        percent = adjusted_percent

                    # Atualizar o máximo apenas se aumentar
                    if percent > self.max_percent_reached:
                        self.max_percent_reached = percent
                    else:
                        # Se o novo percent for menor, usar o máximo anterior
                        percent = self.max_percent_reached

                # Formatar velocidade
                speed_str = None
                if speed:
                    if speed > 1024 * 1024:
                        speed_str = f"{speed / (1024 * 1024):.2f} MB/s"
                    elif speed > 1024:
                        speed_str = f"{speed / 1024:.2f} KB/s"
                    else:
                        speed_str = f"{speed:.2f} B/s"

                # Formatar ETA
                eta_str = None
                if eta:
                    mins, secs = divmod(int(eta), 60)
                    eta_str = f"{mins}m {secs}s"

                progress = DownloadProgress(
                    status='downloading',
                    progress_percent=round(percent, 2),
                    downloaded_bytes=downloaded,
                    total_bytes=total,
                    speed=speed_str,
                    eta=eta_str,
                    current_strategy=self.current_strategy,
                    message=f'Baixando: {percent:.1f}%',
                    filename=d.get('filename')
                )

                self.last_progress = progress

                if self.callback:
                    self.callback(progress)

            elif status == 'finished':
                # Garantir que chegamos a 100%
                self.max_percent_reached = 100.0

                progress = DownloadProgress(
                    status='processing',
                    progress_percent=100.0,
                    current_strategy=self.current_strategy,
                    message='Download concluído, processando arquivo...',
                    filename=d.get('filename')
                )

                self.last_progress = progress

                if self.callback:
                    self.callback(progress)

        except Exception as e:
            logger.error(f"Erro no progress_hook: {e}")

def get_video_info_robust(url: str) -> Dict[str, Any]:
    """Extrai informações com múltiplas estratégias de fallback"""
    normalized_url = normalize_youtube_url(url)
    logger.info(f"Tentando extrair info de: {normalized_url}")

    strategies = [
        {
            'name': 'Android Client',
            'opts': {
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android'],
                    }
                }
            }
        },
        {
            'name': 'Web Client',
            'opts': {
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['web'],
                    }
                }
            }
        },
        {
            'name': 'iOS Client',
            'opts': {
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios'],
                    }
                }
            }
        },
        {
            'name': 'Legacy',
            'opts': {
                'quiet': True,
                'no_warnings': True,
                'youtube_include_dash_manifest': False,
            }
        }
    ]

    last_error = None
    for strategy in strategies:
        try:
            logger.info(f"Tentando estratégia: {strategy['name']}")
            with yt_dlp.YoutubeDL(strategy['opts']) as ydl:
                info = ydl.extract_info(normalized_url, download=False)
                logger.info(f"Sucesso com estratégia: {strategy['name']}")
                return info
        except Exception as e:
            logger.warning(f"Estratégia {strategy['name']} falhou: {str(e)}")
            last_error = e
            continue

    raise HTTPException(status_code=400, detail=f"Todos os métodos falharam. Último erro: {str(last_error)}")

def download_video_robust(url: str, request: VideoRequest, progress_callback: Optional[Callable[[DownloadProgress], None]] = None) -> Dict[str, Any]:
    """Baixa vídeo com múltiplas estratégias de fallback e converte para MP4"""
    normalized_url = normalize_youtube_url(url)
    is_short = is_youtube_short(url)
    logger.info(f"Tentando baixar: {normalized_url} (Short: {is_short})")

    # Inicializar tracker de progresso
    tracker = DownloadProgressTracker(progress_callback)

    # Template simples - deixar yt-dlp decidir o nome temporariamente
    output_template = f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"

    # Estratégias ATUALIZADAS que funcionam com YouTube atual (2024/2025)
    download_strategies = [
        {
            'name': 'MediaConnect Client',
            'opts': {
                'format': 'best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [tracker.progress_hook],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['mediaconnect'],
                    }
                },
                'socket_timeout': 60,
                'retries': 5,
            }
        },
        {
            'name': 'iOS Music Client',
            'opts': {
                'format': 'best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [tracker.progress_hook],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['ios_music'],
                    }
                },
                'socket_timeout': 60,
                'retries': 5,
            }
        },
        {
            'name': 'Android Music Client',
            'opts': {
                'format': 'best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [tracker.progress_hook],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android_music'],
                    }
                },
                'socket_timeout': 60,
                'retries': 5,
            }
        },
        {
            'name': 'Web Client - Modern',
            'opts': {
                'format': 'best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [tracker.progress_hook],
                'extractor_args': {
                    'youtube': {
                        'player_client': ['web'],
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://www.youtube.com/',
                },
                'socket_timeout': 60,
                'retries': 5,
            }
        },
        {
            'name': 'Direct - No Client Override',
            'opts': {
                'format': '(bestvideo[height<=1080]+bestaudio)/best',
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [tracker.progress_hook],
                'merge_output_format': 'mp4',
                'socket_timeout': 60,
                'retries': 5,
            }
        },
    ]

    # Configuração específica para áudio
    if request.audio_only:
        audio_strategies = [
            {
                'name': 'Best Audio',
                'opts': {
                    'format': 'ba/best',
                    'outtmpl': output_template,
                    'quiet': False,
                    'progress_hooks': [tracker.progress_hook],
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'socket_timeout': 60,
                    'retries': 5,
                }
            }
        ]
        download_strategies = audio_strategies

    last_error = None
    for strategy in download_strategies:
        try:
            tracker.set_strategy(strategy['name'])
            logger.info(f"🔄 Tentando download com estratégia: {strategy['name']}")

            with yt_dlp.YoutubeDL(strategy['opts']) as ydl:
                # Primeiro obter info
                info = ydl.extract_info(normalized_url, download=False)

                if not info:
                    logger.warning(f"⚠️ Estratégia {strategy['name']}: Não conseguiu obter informações do vídeo")
                    continue

                # Verificar se tem formatos de vídeo disponíveis (não apenas imagens)
                formats = info.get('formats', [])
                video_formats = [f for f in formats if f.get('vcodec') != 'none' and 'storyboard' not in f.get('format_id', '').lower() and 'sb' != f.get('format_id', '')]

                if not video_formats:
                    logger.warning(f"⚠️ Estratégia {strategy['name']}: Apenas storyboards disponíveis, pulando...")
                    continue

                logger.info(f"✅ Info obtida, iniciando download...")
                logger.info(f"📹 Título: {info.get('title', 'N/A')}")
                logger.info(f"⏱️  Duração: {info.get('duration', 'N/A')} segundos")
                logger.info(f"📊 Formatos de vídeo disponíveis: {len(video_formats)}")

                # Depois fazer download
                ydl.download([normalized_url])

                logger.info(f"✅ Download bem-sucedido com estratégia: {strategy['name']}")

                # Se não for áudio, processar o arquivo
                if not request.audio_only:
                    if progress_callback:
                        progress_callback(DownloadProgress(
                            status='converting',
                            progress_percent=100.0,
                            current_strategy=strategy['name'],
                            message='Convertendo para MP4...'
                        ))

                    final_filename = find_and_convert_latest_video()
                    if final_filename:
                        logger.info(f"✅ Arquivo final processado: {final_filename}")
                        # Validar que o arquivo final tem conteúdo de vídeo real
                        final_path = os.path.join(DOWNLOAD_DIR, final_filename)
                        if os.path.exists(final_path):
                            file_size = os.path.getsize(final_path) / (1024 * 1024)  # MB
                            logger.info(f"📦 Tamanho do arquivo: {file_size:.2f} MB")

                            # Verificar se não é um storyboard (arquivo muito pequeno)
                            if file_size < 1.0:
                                logger.error(f"❌ Arquivo muito pequeno ({file_size:.2f} MB), provavelmente é storyboard")
                                continue

                        if progress_callback:
                            progress_callback(DownloadProgress(
                                status='completed',
                                progress_percent=100.0,
                                current_strategy=strategy['name'],
                                message='Download concluído com sucesso!',
                                filename=final_filename
                            ))

                        return info
                    else:
                        logger.warning("⚠️ Conversão não produziu arquivo final, tentando próxima estratégia...")
                        continue
                else:
                    if progress_callback:
                        progress_callback(DownloadProgress(
                            status='completed',
                            progress_percent=100.0,
                            current_strategy=strategy['name'],
                            message='Download de áudio concluído!'
                        ))
                    return info

        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Estratégia {strategy['name']} falhou: {error_msg}")

            if progress_callback:
                progress_callback(DownloadProgress(
                    status='error',
                    current_strategy=strategy['name'],
                    message=f'Estratégia falhou: {error_msg}'
                ))

            last_error = e
            continue

    raise HTTPException(
        status_code=400,
        detail=f"❌ Todas as estratégias de download falharam. O YouTube pode estar bloqueando o acesso ou o yt-dlp está desatualizado. Execute: pip install --upgrade yt-dlp. Último erro: {str(last_error)}"
    )

def get_available_formats(url: str) -> list:
    """Obtém lista de formatos disponíveis para o vídeo"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'listformats': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            # Filtrar apenas formatos de vídeo válidos
            video_formats = []
            for fmt in formats:
                if (fmt.get('vcodec') and fmt.get('vcodec') != 'none' and
                    fmt.get('ext') in ['mp4', 'webm', 'mkv']):
                    video_formats.append({
                        'format_id': fmt.get('format_id'),
                        'ext': fmt.get('ext'),
                        'quality': fmt.get('height', 0),
                        'vcodec': fmt.get('vcodec'),
                        'acodec': fmt.get('acodec'),
                        'filesize': fmt.get('filesize', 0)
                    })

            logger.info(f"Formatos disponíveis encontrados: {len(video_formats)}")
            return video_formats

    except Exception as e:
        logger.warning(f"Erro ao obter formatos disponíveis: {str(e)}")
        return []

def select_best_format(formats: list) -> str:
    """Seleciona o melhor formato disponível baseado na qualidade e compatibilidade"""
    if not formats:
        return 'best'

    # Ordenar por qualidade (altura) e preferir MP4
    mp4_formats = [f for f in formats if f['ext'] == 'mp4']
    webm_formats = [f for f in formats if f['ext'] == 'webm']

    # Priorizar MP4 com boa qualidade
    if mp4_formats:
        # Ordenar por qualidade decrescente
        mp4_formats.sort(key=lambda x: x['quality'], reverse=True)
        best_mp4 = mp4_formats[0]

        # Se tem qualidade >= 720p, usar esse
        if best_mp4['quality'] >= 720:
            return best_mp4['format_id']

        # Senão, usar o melhor MP4 disponível
        return best_mp4['format_id']

    # Se não tem MP4, usar WebM
    elif webm_formats:
        webm_formats.sort(key=lambda x: x['quality'], reverse=True)
        return webm_formats[0]['format_id']

    # Fallback para o primeiro formato disponível
    formats.sort(key=lambda x: x['quality'], reverse=True)
    return formats[0]['format_id']
