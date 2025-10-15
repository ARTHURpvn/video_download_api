#!/usr/bin/env python3
"""
Script completo para testar e corrigir problemas com FFmpeg e compilação
"""

import subprocess
import sys
import os

def test_ffmpeg():
    """Testar se FFmpeg está instalado"""
    print("🔍 Verificando FFmpeg...\n")

    try:
        if sys.platform == 'win32':
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        else:
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)

        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip().split('\n')[0]
            print(f"✅ FFmpeg encontrado: {ffmpeg_path}")

            # Verificar versão
            version_result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            version = version_result.stdout.split('\n')[0]
            print(f"✅ Versão: {version}\n")

            return True, ffmpeg_path
        else:
            print("❌ FFmpeg NÃO encontrado no PATH\n")
            return False, None
    except Exception as e:
        print(f"❌ Erro ao verificar FFmpeg: {e}\n")
        return False, None

def install_ffmpeg_instructions():
    """Mostrar instruções para instalar FFmpeg"""
    print("="*60)
    print("📝 INSTRUÇÕES PARA INSTALAR FFMPEG")
    print("="*60)

    if sys.platform == 'darwin':  # macOS
        print("\n🍎 macOS:")
        print("   1. Abra o Terminal")
        print("   2. Execute: brew install ffmpeg")
        print("   3. Aguarde a instalação concluir")
        print("   4. Execute este script novamente\n")
    elif sys.platform == 'win32':  # Windows
        print("\n🪟 Windows:")
        print("   1. Baixe FFmpeg em: https://ffmpeg.org/download.html")
        print("   2. Extraia o arquivo")
        print("   3. Adicione ao PATH do sistema")
        print("   4. Reinicie o terminal e execute este script novamente\n")
    else:  # Linux
        print("\n🐧 Linux:")
        print("   1. Execute: sudo apt install ffmpeg")
        print("   2. Ou: sudo yum install ffmpeg")
        print("   3. Execute este script novamente\n")

def main():
    print("="*60)
    print("🎬 TESTE DE CONFIGURAÇÃO - YouTube Downloader")
    print("="*60)
    print()

    # Teste 1: FFmpeg
    has_ffmpeg, ffmpeg_path = test_ffmpeg()

    if not has_ffmpeg:
        install_ffmpeg_instructions()
        print("⚠️  ATENÇÃO: Instale o FFmpeg antes de compilar!")
        print("⚠️  Sem FFmpeg, os vídeos NÃO vão funcionar no executável.\n")

        response = input("❓ Quer continuar mesmo assim? (s/N): ")
        if response.lower() != 's':
            print("\n❌ Operação cancelada.")
            print("💡 Instale o FFmpeg e execute este script novamente.\n")
            sys.exit(1)

    # Teste 2: Python e dependências
    print("\n2️⃣ Verificando ambiente Python...")
    print(f"   ✅ Python: {sys.version.split()[0]}")

    # Verificar se yt-dlp está instalado
    try:
        import yt_dlp
        print(f"   ✅ yt-dlp instalado")
    except ImportError:
        print(f"   ❌ yt-dlp NÃO instalado")
        print(f"      Execute: pip install yt-dlp")

    # Verificar PyInstaller
    try:
        import PyInstaller
        print(f"   ✅ PyInstaller instalado")
    except ImportError:
        print(f"   ❌ PyInstaller NÃO instalado")
        print(f"      Execute: pip install pyinstaller")

    print("\n" + "="*60)

    if has_ffmpeg:
        print("✅ TUDO PRONTO PARA COMPILAR!")
        print("="*60)
        print("\n🚀 Execute agora:")
        print("   python3 build_executable.py\n")
    else:
        print("⚠️  COMPILAÇÃO POSSÍVEL, MAS VÍDEOS PODEM NÃO FUNCIONAR")
        print("="*60)
        print("\n💡 Recomendação: Instale o FFmpeg primeiro!\n")

if __name__ == '__main__':
    main()

