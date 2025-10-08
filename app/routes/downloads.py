from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from ..services.file_manager import list_all_downloads, delete_file, get_file_path
from ..utils.config import DOWNLOAD_DIR

router = APIRouter(prefix="/downloads", tags=["downloads"])

@router.get("")
async def list_downloads():
    """Lista todos os arquivos baixados"""
    return list_all_downloads()

@router.get("/{filename}")
async def download_file(filename: str):
    """Baixa um arquivo específico"""
    try:
        file_path = get_file_path(filename)

        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"Arquivo '{filename}' não encontrado")

        # Verificar se é realmente um arquivo (não um diretório)
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail=f"'{filename}' não é um arquivo válido")

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
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar arquivo: {str(e)}")

@router.delete("/{filename}")
async def delete_download(filename: str):
    """Deleta um arquivo baixado"""
    return delete_file(filename)
