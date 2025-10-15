#!/usr/bin/env python3
"""
Script para criar executável standalone do YouTube Downloader
Usa PyInstaller para empacotar a aplicação
"""

import PyInstaller.__main__
import os
import shutil
import sys
import subprocess
from pathlib import Path

def find_ffmpeg():
    """Localizar FFmpeg no sistema"""
    try:
        # Tentar encontrar FFmpeg
        if sys.platform == 'win32':
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        else:
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)

        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip().split('\n')[0]
            print(f"✅ FFmpeg encontrado em: {ffmpeg_path}")
            return ffmpeg_path
        else:
            print("⚠️  FFmpeg não encontrado no PATH")
            return None
    except Exception as e:
        print(f"⚠️  Erro ao procurar FFmpeg: {e}")
        return None

def build_executable():
    """Criar executável com PyInstaller"""

    print("🚀 Iniciando build do executável...")

    # Localizar FFmpeg
    ffmpeg_path = find_ffmpeg()

    # Limpar builds anteriores
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Determinar extensão do executável baseado no SO
    exe_extension = '.exe' if sys.platform == 'win32' else ''

    # Opções do PyInstaller
    pyinstaller_args = [
        'gui_app.py',  # Script principal
        '--name=YouTubeDownloader',  # Nome do executável
        '--onefile',  # Criar um único arquivo
        '--windowed',  # Sem console (apenas GUI)
        '--clean',  # Limpar cache
        '--noconfirm',  # Não pedir confirmação

        # Adicionar módulos necessários - MAIS COMPLETO
        '--hidden-import=uvicorn',
        '--hidden-import=uvicorn.logging',
        '--hidden-import=uvicorn.loops',
        '--hidden-import=uvicorn.loops.auto',
        '--hidden-import=uvicorn.protocols',
        '--hidden-import=uvicorn.protocols.http',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.lifespan.on',

        '--hidden-import=fastapi',
        '--hidden-import=fastapi.routing',
        '--hidden-import=fastapi.responses',
        '--hidden-import=starlette',
        '--hidden-import=starlette.routing',
        '--hidden-import=starlette.responses',
        '--hidden-import=starlette.middleware',
        '--hidden-import=starlette.middleware.cors',
        '--hidden-import=starlette.applications',

        '--hidden-import=yt_dlp',
        '--hidden-import=yt_dlp.extractor',
        '--hidden-import=yt_dlp.downloader',

        '--hidden-import=pydantic',
        '--hidden-import=pydantic.fields',
        '--hidden-import=pydantic.main',

        '--hidden-import=multipart',
        '--hidden-import=python_multipart',

        # Dependências críticas do uvicorn
        '--hidden-import=asyncio',
        '--hidden-import=h11',
        '--hidden-import=httptools',
        '--hidden-import=websockets',
        '--hidden-import=watchfiles',
        '--hidden-import=click',

        # Módulos do app
        '--hidden-import=app',
        '--hidden-import=app.main',
        '--hidden-import=app.routes',
        '--hidden-import=app.routes.video',
        '--hidden-import=app.routes.downloads',
        '--hidden-import=app.routes.health',
        '--hidden-import=app.services',
        '--hidden-import=app.services.youtube',
        '--hidden-import=app.services.file_manager',
        '--hidden-import=app.models',
        '--hidden-import=app.models.schemas',
        '--hidden-import=app.utils',
        '--hidden-import=app.utils.config',
        '--hidden-import=app.utils.helpers',

        # Incluir diretório app completo como dados
        '--add-data=app:app' if sys.platform != 'win32' else '--add-data=app;app',

        # Coletar todos os submódulos
        '--collect-all=uvicorn',
        '--collect-all=fastapi',
        '--collect-all=starlette',
        '--collect-all=yt_dlp',
        '--collect-all=h11',
        '--collect-all=httptools',

        # Copiar metadados
        '--copy-metadata=uvicorn',
        '--copy-metadata=fastapi',
        '--copy-metadata=starlette',
        '--copy-metadata=yt_dlp',
        '--copy-metadata=h11',
        '--copy-metadata=httptools',

        # Recursivo para pegar tudo
        '--recursive-copy-metadata=uvicorn',
        '--recursive-copy-metadata=fastapi',
    ]

    # ADICIONAR FFMPEG AO EXECUTÁVEL SE DISPONÍVEL
    if ffmpeg_path and os.path.exists(ffmpeg_path):
        print("📦 Incluindo FFmpeg no executável...")
        separator = ';' if sys.platform == 'win32' else ':'
        pyinstaller_args.append(f'--add-binary={ffmpeg_path}{separator}.')

        # Também tentar incluir ffprobe se existir
        ffprobe_path = ffmpeg_path.replace('ffmpeg', 'ffprobe')
        if os.path.exists(ffprobe_path):
            pyinstaller_args.append(f'--add-binary={ffprobe_path}{separator}.')
            print(f"📦 Incluindo FFprobe no executável...")
    else:
        print("\n⚠️  AVISO: FFmpeg não foi encontrado!")
        print("⚠️  O executável pode não conseguir processar vídeos corretamente.")
        print("\n📝 Para instalar FFmpeg:")
        if sys.platform == 'darwin':
            print("   brew install ffmpeg")
        elif sys.platform == 'win32':
            print("   1. Baixe em: https://ffmpeg.org/download.html")
            print("   2. Extraia e adicione ao PATH")
        else:
            print("   sudo apt install ffmpeg")

        response = input("\n❓ Continuar mesmo assim? (s/N): ")
        if response.lower() != 's':
            print("❌ Build cancelado.")
            return False

    # Executar PyInstaller
    print("\n📦 Empacotando aplicação...")
    print("⚠️  Isso pode levar 10-15 minutos...")
    try:
        PyInstaller.__main__.run(pyinstaller_args)
    except Exception as e:
        print(f"\n❌ Erro ao criar executável: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Determinar local de destino baseado no SO
    desktop = Path.home() / 'Desktop'

    if sys.platform == 'win32':
        # Windows: Copiar direto para a área de trabalho
        dest_exe = desktop / f'YouTubeDownloader{exe_extension}'
    elif sys.platform == 'darwin':
        # macOS: Copiar para área de trabalho
        dest_exe = desktop / 'YouTubeDownloader'
    else:
        # Linux: Copiar para área de trabalho
        dest_exe = desktop / 'YouTubeDownloader'

    # Mover executável para o destino
    exe_name = f'YouTubeDownloader{exe_extension}'
    source_exe = Path('dist') / exe_name

    if source_exe.exists():
        print(f"\n📦 Copiando executável para Área de Trabalho...")
        shutil.copy2(source_exe, dest_exe)

        # Tornar executável no Linux/macOS
        if sys.platform != 'win32':
            os.chmod(dest_exe, 0o755)

        print("\n✅ Build completo!")
        print(f"📁 Executável criado em: {dest_exe}")

        if sys.platform == 'win32':
            print("\n📝 Instruções:")
            print("   1. Vá até sua Área de Trabalho")
            print("   2. Duplo clique em 'YouTubeDownloader.exe'")
            print("   3. Aguarde ~10 segundos para o servidor iniciar")
            print("   4. Cole um link do YouTube e baixe!")
        else:
            print("\n📝 Instruções:")
            print("   1. Vá até sua Área de Trabalho")
            print("   2. Duplo clique em 'YouTubeDownloader'")
            print("   3. Aguarde ~10 segundos para o servidor iniciar")
            print("   4. Cole um link do YouTube e baixe!")

        return True
    else:
        print(f"\n❌ Erro: Executável não encontrado em {source_exe}")
        return False

if __name__ == '__main__':
    success = build_executable()
    sys.exit(0 if success else 1)
