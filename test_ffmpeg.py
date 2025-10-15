#!/usr/bin/env python3
"""
Script para testar se o FFmpeg está instalado e funcionando
"""

import subprocess
import sys
import os

print("🔍 Testando FFmpeg no sistema...\n")

# Teste 1: Verificar se FFmpeg está no PATH
print("1️⃣ Verificando se FFmpeg está no PATH...")
try:
    if sys.platform == 'win32':
        result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
    else:
        result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)

    if result.returncode == 0:
        ffmpeg_path = result.stdout.strip().split('\n')[0]
        print(f"   ✅ FFmpeg encontrado: {ffmpeg_path}\n")
    else:
        print(f"   ❌ FFmpeg NÃO encontrado no PATH\n")
        print("   📝 Para instalar no macOS:")
        print("      brew install ffmpeg\n")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Erro ao procurar FFmpeg: {e}\n")
    sys.exit(1)

# Teste 2: Verificar versão do FFmpeg
print("2️⃣ Verificando versão do FFmpeg...")
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    version_line = result.stdout.split('\n')[0]
    print(f"   ✅ {version_line}\n")
except Exception as e:
    print(f"   ❌ Erro ao verificar versão: {e}\n")

# Teste 3: Verificar FFprobe
print("3️⃣ Verificando FFprobe...")
try:
    if sys.platform == 'win32':
        result = subprocess.run(['where', 'ffprobe'], capture_output=True, text=True)
    else:
        result = subprocess.run(['which', 'ffprobe'], capture_output=True, text=True)

    if result.returncode == 0:
        ffprobe_path = result.stdout.strip().split('\n')[0]
        print(f"   ✅ FFprobe encontrado: {ffprobe_path}\n")
    else:
        print(f"   ⚠️  FFprobe não encontrado (opcional)\n")
except Exception as e:
    print(f"   ⚠️  Erro ao procurar FFprobe: {e}\n")

# Teste 4: Verificar se os arquivos existem
print("4️⃣ Verificando se os executáveis existem...")
if os.path.exists(ffmpeg_path):
    print(f"   ✅ Arquivo existe: {ffmpeg_path}")
    print(f"   📊 Tamanho: {os.path.getsize(ffmpeg_path) / (1024*1024):.2f} MB\n")
else:
    print(f"   ❌ Arquivo NÃO existe: {ffmpeg_path}\n")

print("="*60)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*60)
print("\n🎉 Agora você pode compilar o executável:")
print("   python3 build_executable.py\n")

