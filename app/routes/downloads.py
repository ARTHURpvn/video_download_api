from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import logging
from ..services.file_manager import list_all_downloads, delete_file, get_file_path
from ..utils.config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/downloads", tags=["downloads"])

@router.get("")
async def list_downloads():
    """Lista todos os arquivos baixados"""
    try:
        return list_all_downloads()
    except Exception as e:
        logger.error(f"Erro ao listar downloads: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{filename}")
async def download_file(filename: str):
    """Baixa um arquivo específico"""
    try:
        file_path = get_file_path(filename)

        logger.info(f"📥 Requisição de download: {filename}")
        logger.info(f"📁 Caminho completo: {file_path}")

        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            logger.warning(f"❌ Arquivo não encontrado: {file_path}")
            raise HTTPException(status_code=404, detail=f"Arquivo '{filename}' não encontrado")

        # Verificar se é realmente um arquivo (não um diretório)
        if not os.path.isfile(file_path):
            logger.warning(f"❌ Não é um arquivo válido: {file_path}")
            raise HTTPException(status_code=400, detail=f"'{filename}' não é um arquivo válido")

        # Obter tamanho do arquivo
        file_size = os.path.getsize(file_path)
        logger.info(f"📊 Tamanho do arquivo: {file_size / (1024*1024):.2f} MB")

        # Determinar o media type baseado na extensão
        media_type = "application/octet-stream"
        if filename.endswith('.mp4'):
            media_type = "video/mp4"
        elif filename.endswith('.mp3'):
            media_type = "audio/mpeg"
        elif filename.endswith('.webm'):
            media_type = "video/webm"

        # Retornar o arquivo
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao baixar arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao baixar arquivo: {str(e)}")

@router.delete("/{filename}")
async def delete_download(filename: str):
    """Remove um arquivo baixado"""
    try:
        success = delete_file(filename)
        if success:
            logger.info(f"🗑️ Arquivo deletado: {filename}")
            return {"status": "success", "message": f"Arquivo '{filename}' deletado com sucesso"}
        else:
            raise HTTPException(status_code=404, detail=f"Arquivo '{filename}' não encontrado")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao deletar arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}")
