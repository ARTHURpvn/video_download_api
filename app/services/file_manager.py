import os
import logging
from typing import List, Dict, Any, Optional
from fastapi import HTTPException

from ..utils.config import DOWNLOAD_DIR
from ..utils.helpers import sanitize_filename
from ..services.video_converter import find_and_convert_latest_video

logger = logging.getLogger(__name__)

def find_downloaded_file(title: str) -> Optional[str]:
    """Encontra o arquivo baixado mais recente e garante que está em MP4"""
    try:
        # Usar a nova função de conversão que encontra e converte automaticamente
        final_filename = find_and_convert_latest_video()
        return final_filename
    except Exception as e:
        logger.warning(f"Erro ao encontrar arquivo: {e}")
        return None

def list_all_downloads() -> Dict[str, Any]:
    """Lista todos os arquivos baixados"""
    try:
        files = []
        for filename in os.listdir(DOWNLOAD_DIR):
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size_mb": round(file_stat.st_size / (1024 * 1024), 2),
                    "created_at": file_stat.st_ctime
                })

        return {"downloads": files, "total": len(files)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar downloads: {str(e)}")

def delete_file(filename: str) -> Dict[str, str]:
    """Deleta um arquivo específico"""
    try:
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"status": "success", "message": f"Arquivo {filename} deletado com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar arquivo: {str(e)}")

def get_file_path(filename: str) -> str:
    """Retorna o caminho completo do arquivo"""
    return os.path.join(DOWNLOAD_DIR, filename)
