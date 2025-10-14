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
            print("   2. Clique duas vezes em 'YouTubeDownloader.exe'")
            print("   3. Aguarde alguns segundos para o aplicativo abrir")
        else:
            print("\n📝 Instruções:")
            print("   1. Vá até sua Área de Trabalho")
            print("   2. Clique duas vezes em 'YouTubeDownloader'")
            print("   3. Aguarde alguns segundos para o aplicativo abrir")

        return True
    else:
        print(f"\n❌ Erro: Executável não encontrado em {source_exe}")
        return False

if __name__ == "__main__":
    success = build_executable()
    sys.exit(0 if success else 1)
