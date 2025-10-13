#!/usr/bin/env python3
"""
Script para criar executável standalone do YouTube Downloader
Usa PyInstaller para empacotar a aplicação
"""

import PyInstaller.__main__
import os
import shutil
import sys
from pathlib import Path

def build_executable():
    """Criar executável com PyInstaller"""

    print("🚀 Iniciando build do executável...")

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

        # Adicionar módulos necessários
        '--hidden-import=uvicorn',
        '--hidden-import=fastapi',
        '--hidden-import=yt_dlp',
        '--hidden-import=moviepy',
        '--hidden-import=app',
        '--hidden-import=app.main',
        '--hidden-import=app.routes',
        '--hidden-import=app.services',
        '--hidden-import=app.models',
        '--hidden-import=app.utils',

        # Incluir diretório app completo
        '--add-data=app:app' if sys.platform != 'win32' else '--add-data=app;app',

        # Ícone (opcional - descomentar se tiver um ícone)
        # '--icon=icon.ico',
    ]

    # Executar PyInstaller
    print("📦 Empacotando aplicação...")
    try:
        PyInstaller.__main__.run(pyinstaller_args)
    except Exception as e:
        print(f"\n❌ Erro ao criar executável: {e}")
        return False

    # Determinar local de destino baseado no SO
    if sys.platform == 'win32':
        # Windows: Desktop do usuário
        desktop = Path.home() / 'Desktop'
        dest_folder = desktop / 'YouTubeDownloader'
    elif sys.platform == 'darwin':
        # macOS: Applications ou Desktop
        dest_folder = Path.home() / 'Desktop' / 'YouTubeDownloader'
    else:
        # Linux: Home do usuário
        dest_folder = Path.home() / 'YouTubeDownloader'

    # Criar pasta de destino
    dest_folder.mkdir(parents=True, exist_ok=True)

    # Mover executável para o destino
    exe_name = f'YouTubeDownloader{exe_extension}'
    source_exe = Path('dist') / exe_name
    dest_exe = dest_folder / exe_name

    if source_exe.exists():
        print(f"\n📦 Movendo executável para: {dest_folder}")
        shutil.copy2(source_exe, dest_exe)

        # Tornar executável no Linux/macOS
        if sys.platform != 'win32':
            os.chmod(dest_exe, 0o755)

    print("\n✅ Build completo!")
    print(f"📁 Executável criado em: {dest_exe}")

    if sys.platform == 'win32':
        print(f"\n📍 O executável foi salvo na pasta:")
        print(f"   {dest_folder}")
        print("\n📝 Instruções:")
        print("   1. Vá até a pasta 'YouTubeDownloader' na sua Área de Trabalho")
        print("   2. Clique duas vezes em 'YouTubeDownloader.exe' para executar")
        print("   3. Você pode criar um atalho na área de trabalho se desejar")
    else:
        print("\n📝 Instruções:")
        print("   1. O executável está na pasta indicada acima")
        print("   2. Você pode mover o arquivo para qualquer lugar")
        print("   3. Clique duas vezes para executar")

    print("\n⚠️  Nota: FFmpeg será baixado automaticamente se necessário")

    return True


if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
