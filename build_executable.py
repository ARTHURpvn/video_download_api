#!/usr/bin/env python3
"""
Script para criar executável standalone do YouTube Downloader
Usa PyInstaller para empacotar a aplicação
"""

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build_executable():
    """Criar executável com PyInstaller"""

    print("🚀 Iniciando build do executável...")

    # Limpar builds anteriores
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

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
        '--add-data=app:app',

        # Ícone (opcional - descomentar se tiver um ícone)
        # '--icon=icon.ico',
    ]

    # Executar PyInstaller
    print("📦 Empacotando aplicação...")
    PyInstaller.__main__.run(pyinstaller_args)

    print("\n✅ Build completo!")
    print(f"📁 Executável criado em: dist/YouTubeDownloader")
    print("\n📝 Instruções:")
    print("   1. O executável está na pasta 'dist'")
    print("   2. Você pode mover o arquivo para qualquer lugar")
    print("   3. Clique duas vezes para executar")
    print("\n⚠️  Nota: FFmpeg ainda precisa estar instalado no sistema")
    print("   - macOS: brew install ffmpeg")
    print("   - Windows: baixar de ffmpeg.org")
    print("   - Linux: apt install ffmpeg ou yum install ffmpeg")


if __name__ == "__main__":
    build_executable()

