import os
import logging
import glob
import subprocess
from typing import Optional

from ..utils.config import DOWNLOAD_DIR
from ..utils.helpers import generate_video_filename
from ..utils.ffmpeg_locator import get_ffmpeg_path, get_ffprobe_path

logger = logging.getLogger(__name__)

def convert_with_ffmpeg(input_file: str, target_filename: str) -> str:
    """Converte usando ffmpeg com configurações otimizadas para preservar vídeo completo"""
    try:
        input_path = os.path.join(DOWNLOAD_DIR, input_file)
        output_path = os.path.join(DOWNLOAD_DIR, target_filename)

        logger.info(f"Convertendo {input_file} para {target_filename} usando ffmpeg")

        # 🔧 Usar o localizador de FFmpeg
        ffmpeg_cmd = get_ffmpeg_path()
        logger.info(f"🎬 Usando FFmpeg: {ffmpeg_cmd}")

        # Comando ffmpeg SIMPLIFICADO - apenas copia streams sem recodificar
        # Isso evita perda de frames e garante que o vídeo completo seja preservado
        cmd = [
            ffmpeg_cmd,  # 🔧 MODIFICADO
            '-y',  # sobrescrever arquivo se existir
            '-i', input_path,
            '-c', 'copy',  # COPIAR streams sem recodificar (mais rápido e sem perda)
            '-movflags', '+faststart',  # otimizado para streaming
            output_path
        ]

        logger.info(f"Executando: {' '.join(cmd)}")

        # Executar comando ffmpeg
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"✅ Conversão bem-sucedida: {target_filename}")
            try:
                os.remove(input_path)
                logger.info(f"Arquivo original {input_file} removido")
            except:
                pass
            return target_filename
        else:
            logger.error(f"Erro na conversão ffmpeg: {result.stderr}")
            # Se falhou com -c copy, tentar recodificando
            logger.info("Tentando recodificar com ffmpeg...")
            return convert_with_ffmpeg_reencode(input_file, target_filename)

    except subprocess.TimeoutExpired:
        logger.error("Timeout na conversão ffmpeg")
        return input_file
    except Exception as e:
        logger.error(f"Erro na conversão ffmpeg: {str(e)}")
        return input_file

def convert_with_ffmpeg_reencode(input_file: str, target_filename: str) -> str:
    """Recodifica o vídeo se a cópia simples falhar"""
    try:
        input_path = os.path.join(DOWNLOAD_DIR, input_file)
        output_path = os.path.join(DOWNLOAD_DIR, target_filename)

        logger.info(f"Recodificando {input_file} para {target_filename}")

        # 🔧 Usar o localizador de FFmpeg
        ffmpeg_cmd = get_ffmpeg_path()

        cmd = [
            ffmpeg_cmd,  # 🔧 MODIFICADO
            '-y',
            '-i', input_path,
            '-c:v', 'libx264',  # codec de vídeo
            '-preset', 'fast',  # preset rápido
            '-crf', '23',  # qualidade boa
            '-c:a', 'aac',  # codec de áudio
            '-b:a', '128k',  # bitrate de áudio
            '-movflags', '+faststart',
            output_path
        ]

        logger.info(f"Executando: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"✅ Recodificação bem-sucedida: {target_filename}")
            try:
                os.remove(input_path)
            except:
                pass
            return target_filename
        else:
            logger.error(f"Erro na recodificação: {result.stderr}")
            return input_file

    except Exception as e:
        logger.error(f"Erro na recodificação: {str(e)}")
        return input_file

def convert_to_mp4(input_file: str, target_filename: str) -> str:
    """Converte qualquer arquivo de vídeo para MP4 - versão robusta"""
    try:
        input_path = os.path.join(DOWNLOAD_DIR, input_file)
        output_path = os.path.join(DOWNLOAD_DIR, target_filename)

        # Se o arquivo tem extensão problemática (.mhtml), usar ffmpeg diretamente
        if input_file.lower().endswith('.mhtml'):
            return convert_with_ffmpeg(input_file, target_filename)

        logger.info(f"Convertendo {input_file} para {target_filename} usando moviepy")

        # Tentar com moviepy primeiro para outros formatos
        try:
            from moviepy.editor import VideoFileClip

            with VideoFileClip(input_path) as video:
                video.write_videofile(
                    output_path,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )

            # Remover arquivo original se conversão foi bem-sucedida
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                try:
                    os.remove(input_path)
                    logger.info(f"Arquivo original {input_file} removido")
                except:
                    pass
                return target_filename
            else:
                # Se moviepy falhou, tentar ffmpeg
                logger.warning("MoviePy falhou, tentando ffmpeg")
                return convert_with_ffmpeg(input_file, target_filename)

        except Exception as moviepy_error:
            logger.warning(f"MoviePy falhou: {str(moviepy_error)}, tentando ffmpeg")
            return convert_with_ffmpeg(input_file, target_filename)

    except Exception as e:
        logger.error(f"Erro geral na conversão: {str(e)}")
        return input_file

def validate_video_file(file_path: str) -> bool:
    """Valida se o arquivo é um vídeo real com duração > 0 e movimento"""
    try:
        # 🔧 Usar o localizador de FFprobe
        ffprobe_cmd = get_ffprobe_path()

        # Verificar duração básica
        cmd_duration = [
            ffprobe_cmd,  # 🔧 MODIFICADO
            '-v', 'quiet',
            '-show_entries', 'format=duration',
            '-of', 'csv=p=0',
            file_path
        ]

        result = subprocess.run(cmd_duration, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return False

        duration_str = result.stdout.strip()
        if not duration_str or duration_str == 'N/A':
            return False

        duration = float(duration_str)
        logger.info(f"Duração do arquivo: {duration} segundos")

        if duration <= 0:
            return False

        # Verificar se tem frames de vídeo reais (não apenas uma imagem)
        cmd_frames = [
            ffprobe_cmd,  # 🔧 MODIFICADO
            '-v', 'quiet',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=nb_frames,r_frame_rate',
            '-of', 'csv=p=0',
            file_path
        ]

        result_frames = subprocess.run(cmd_frames, capture_output=True, text=True, timeout=30)

        if result_frames.returncode == 0:
            output_lines = result_frames.stdout.strip().split('\n')
            for line in output_lines:
                if line and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        try:
                            nb_frames = int(parts[0]) if parts[0] != 'N/A' else 0
                            if nb_frames > 10:  # Pelo menos 10 frames para ser considerado vídeo
                                logger.info(f"Arquivo válido: {nb_frames} frames")
                                return True
                        except ValueError:
                            continue

        logger.warning(f"Arquivo {file_path} parece ser uma imagem estática")
        return False

    except Exception as e:
        logger.error(f"Erro ao validar arquivo: {str(e)}")
        return False

def find_and_convert_latest_video() -> Optional[str]:
    """Encontra o último arquivo baixado e renomeia/converte para MP4 se necessário"""
    try:
        # Procurar todos os arquivos de vídeo na pasta
        video_extensions = ['*.mp4', '*.mkv', '*.avi', '*.mov', '*.flv', '*.webm', '*.mhtml', '*.m4v', '*.3gp', '*.ts']
        all_files = []

        for ext in video_extensions:
            files = glob.glob(os.path.join(DOWNLOAD_DIR, ext))
            all_files.extend(files)

        if not all_files:
            logger.warning("Nenhum arquivo de vídeo encontrado")
            return None

        # Pegar o arquivo mais recente
        latest_file = max(all_files, key=os.path.getctime)
        filename = os.path.basename(latest_file)

        logger.info(f"📁 Arquivo mais recente encontrado: {filename}")

        # Verificar tamanho do arquivo baixado
        file_size_mb = os.path.getsize(latest_file) / (1024 * 1024)
        logger.info(f"📊 Tamanho do arquivo baixado: {file_size_mb:.2f} MB")

        # VALIDAÇÃO CRÍTICA: Rejeitar arquivos muito pequenos (storyboards)
        if file_size_mb < 1.0:
            logger.error(f"❌ STORYBOARD DETECTADO: Arquivo muito pequeno ({file_size_mb:.2f} MB)")
            logger.error("❌ O YouTube bloqueou o download do vídeo real, apenas thumbnails foram baixadas")
            os.remove(latest_file)
            return None

        # DIAGNÓSTICO: Verificar o arquivo com ffprobe ANTES de qualquer operação
        logger.info("🔍 Diagnosticando arquivo baixado com ffprobe...")
        try:
            cmd_probe = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'stream=codec_type,codec_name,width,height,duration,nb_frames',
                '-show_entries', 'format=duration,size,bit_rate',
                '-of', 'json',
                latest_file
            ]
            result = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                logger.info(f"📋 Informações do arquivo baixado:\n{result.stdout}")

                # Validar se é um vídeo real (não MJPEG/storyboard)
                import json
                probe_data = json.loads(result.stdout)
                streams = probe_data.get('streams', [])

                for stream in streams:
                    if stream.get('codec_type') == 'video':
                        codec_name = stream.get('codec_name', '')
                        nb_frames = int(stream.get('nb_frames', 0))
                        duration = float(stream.get('duration', 0))

                        # MJPEG com poucos frames = storyboard
                        if codec_name == 'mjpeg' and nb_frames < 100:
                            logger.error(f"❌ STORYBOARD DETECTADO: Codec MJPEG com apenas {nb_frames} frames")
                            logger.error("❌ Não é um vídeo real, removendo arquivo...")
                            os.remove(latest_file)
                            return None

                        # Duração muito curta = problema
                        if duration < 5.0:
                            logger.error(f"❌ STORYBOARD DETECTADO: Duração muito curta ({duration:.2f}s)")
                            logger.error("❌ Não é um vídeo real, removendo arquivo...")
                            os.remove(latest_file)
                            return None

            else:
                logger.error(f"❌ Erro ao diagnosticar arquivo: {result.stderr}")
        except Exception as probe_error:
            logger.error(f"❌ Erro ao executar ffprobe: {probe_error}")

        # Gerar nome alvo
        target_filename = generate_video_filename("mp4")

        # Se já é MP4, apenas RENOMEAR (não converter)
        if filename.endswith('.mp4'):
            target_path = os.path.join(DOWNLOAD_DIR, target_filename)
            logger.info(f"📝 Arquivo já é MP4, renomeando de {filename} para {target_filename}")
            try:
                os.rename(latest_file, target_path)
                logger.info(f"✅ Renomeado com sucesso: {target_filename}")

                # Verificar o arquivo renomeado
                if os.path.exists(target_path):
                    final_size_mb = os.path.getsize(target_path) / (1024 * 1024)
                    logger.info(f"✅ Tamanho do arquivo final: {final_size_mb:.2f} MB")

                return target_filename
            except Exception as e:
                logger.error(f"❌ Erro ao renomear: {e}")
                return filename

        # Se NÃO é MP4, então converter usando ffmpeg (cópia de streams)
        logger.info(f"🔄 Arquivo não é MP4 ({filename}), convertendo para {target_filename}")
        converted_filename = convert_with_ffmpeg(filename, target_filename)

        if converted_filename == target_filename:
            logger.info(f"✅ Conversão bem-sucedida: {converted_filename}")
            return converted_filename
        else:
            logger.warning(f"⚠️ Conversão falhou, mantendo arquivo original: {filename}")
            return filename

    except Exception as e:
        logger.error(f"❌ Erro ao encontrar/processar vídeo: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None
