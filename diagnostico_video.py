#!/usr/bin/env python3
"""
Script de diagnóstico para problemas com vídeos no executável
"""

import subprocess
import sys
import os

def check_ffmpeg_location():
    """Verificar onde o FFmpeg está instalado"""
    print("="*60)
    print("🔍 DIAGNÓSTICO: Localização do FFmpeg")
    print("="*60)

    locations_to_check = [
        '/opt/homebrew/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/usr/bin/ffmpeg',
    ]

    for location in locations_to_check:
        if os.path.exists(location):
            print(f"✅ Encontrado em: {location}")
        else:
            print(f"❌ NÃO existe: {location}")

    # Verificar usando which
    try:
        result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0:
            actual_path = result.stdout.strip()
            print(f"\n💡 PATH real do sistema: {actual_path}")

            # Verificar se é um link simbólico
            if os.path.islink(actual_path):
                real_path = os.path.realpath(actual_path)
                print(f"   → Link aponta para: {real_path}")
                return real_path
            return actual_path
        else:
            print("\n❌ FFmpeg não encontrado no PATH do sistema")
            return None
    except Exception as e:
        print(f"\n❌ Erro ao verificar: {e}")
        return None

def check_spec_file():
    """Verificar o arquivo .spec"""
    print("\n" + "="*60)
    print("📝 DIAGNÓSTICO: Arquivo YouTubeDownloader.spec")
    print("="*60)

    spec_file = 'YouTubeDownloader.spec'
    if not os.path.exists(spec_file):
        print("❌ Arquivo .spec não encontrado!")
        return None

    with open(spec_file, 'r') as f:
        content = f.read()

    # Procurar pela linha de binaries
    if '/opt/homebrew/bin/ffmpeg' in content:
        print("⚠️  Encontrado: binaries usa /opt/homebrew/bin/ffmpeg")
        print("   Isso só funciona se o FFmpeg estiver nesse local exato!")

    if "binaries = [" in content:
        # Extrair a linha de binaries
        for line in content.split('\n'):
            if 'binaries = [' in line and 'ffmpeg' in line:
                print(f"\n📋 Linha atual:")
                print(f"   {line.strip()}")

    return content

def check_yt_dlp_config():
    """Verificar se yt-dlp está configurado para usar FFmpeg"""
    print("\n" + "="*60)
    print("🎬 DIAGNÓSTICO: Configuração do yt-dlp")
    print("="*60)

    # Procurar por arquivos que usam yt-dlp
    py_files = []
    for root, dirs, files in os.walk('app'):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))

    # Adicionar arquivos na raiz
    for file in ['gui_app.py', 'build_executable.py']:
        if os.path.exists(file):
            py_files.append(file)

    found_ytdlp = False
    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                content = f.read()

            if 'yt_dlp' in content or 'yt-dlp' in content:
                found_ytdlp = True
                print(f"\n📄 Arquivo: {py_file}")

                # Verificar se define ffmpeg_location
                if 'ffmpeg_location' in content:
                    print("   ✅ Usa 'ffmpeg_location'")
                    # Mostrar a linha
                    for line in content.split('\n'):
                        if 'ffmpeg_location' in line and not line.strip().startswith('#'):
                            print(f"      {line.strip()}")
                else:
                    print("   ❌ NÃO configura 'ffmpeg_location'")
                    print("      Isso é CRÍTICO para o executável funcionar!")

                # Verificar postprocessors
                if 'postprocessors' in content:
                    print("   ✅ Usa 'postprocessors'")

                # Verificar YoutubeDL options
                if 'YoutubeDL' in content:
                    print("   ✅ Usa YoutubeDL")

    if not found_ytdlp:
        print("❌ Nenhum arquivo usando yt-dlp encontrado!")

    return found_ytdlp

def main():
    print("\n" + "="*60)
    print("🎯 DIAGNÓSTICO COMPLETO - Problema com Vídeos")
    print("="*60)
    print()

    # 1. Verificar FFmpeg
    ffmpeg_path = check_ffmpeg_location()

    # 2. Verificar arquivo .spec
    spec_content = check_spec_file()

    # 3. Verificar configuração do yt-dlp
    has_ytdlp = check_yt_dlp_config()

    # Resumo e soluções
    print("\n" + "="*60)
    print("🔧 PROBLEMAS IDENTIFICADOS E SOLUÇÕES")
    print("="*60)

    if ffmpeg_path and ffmpeg_path != '/opt/homebrew/bin/ffmpeg':
        print("\n⚠️  PROBLEMA 1: FFmpeg está em local diferente do .spec")
        print(f"   Local real: {ffmpeg_path}")
        print(f"   Local no .spec: /opt/homebrew/bin/ffmpeg")
        print("\n   SOLUÇÃO: Atualizar o arquivo .spec com o caminho correto:")
        print(f"   binaries = [('{ffmpeg_path}', '.'), ('{ffmpeg_path.replace('ffmpeg', 'ffprobe')}', '.')]")

    print("\n⚠️  PROBLEMA 2: yt-dlp precisa saber onde está o FFmpeg no executável")
    print("   Quando compilado, o FFmpeg fica dentro do bundle do executável")
    print("\n   SOLUÇÃO: Configurar 'ffmpeg_location' no código Python:")
    print("   ydl_opts = {")
    print("       'ffmpeg_location': get_ffmpeg_path(),  # Função que detecta se está no executável")
    print("       # ... outras opções")
    print("   }")

    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Vou criar uma correção automática para todos os arquivos")
    print("   2. Você precisará recompilar o executável")
    print("   3. O vídeo funcionará no executável")

    return ffmpeg_path

if __name__ == '__main__':
    ffmpeg_path = main()

    print("\n" + "="*60)
    print("✅ Diagnóstico concluído!")
    print("="*60)
    print()

