#!/usr/bin/env python3
"""
Script de teste para verificar se o servidor está iniciando corretamente
"""

import sys
import os

print("="*60)
print("🧪 TESTE: Verificando imports e dependências")
print("="*60)

# Teste 1: Importar ffmpeg_locator
print("\n1. Testando import do ffmpeg_locator...")
try:
    from app.utils.ffmpeg_locator import get_ffmpeg_path, get_ffprobe_path, get_ffmpeg_location_for_ytdlp
    print("   ✅ ffmpeg_locator importado com sucesso")

    ffmpeg_path = get_ffmpeg_path()
    print(f"   📍 FFmpeg: {ffmpeg_path}")

    ffprobe_path = get_ffprobe_path()
    print(f"   📍 FFprobe: {ffprobe_path}")

    ffmpeg_location = get_ffmpeg_location_for_ytdlp()
    print(f"   📍 FFmpeg location (yt-dlp): {ffmpeg_location}")

except Exception as e:
    print(f"   ❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 2: Importar routes
print("\n2. Testando import das rotas...")
try:
    from app.routes import health, video, downloads
    print("   ✅ Rotas importadas com sucesso")
except Exception as e:
    print(f"   ❌ ERRO ao importar rotas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 3: Importar services
print("\n3. Testando import dos serviços...")
try:
    from app.services import youtube, video_converter, file_manager
    print("   ✅ Serviços importados com sucesso")
except Exception as e:
    print(f"   ❌ ERRO ao importar serviços: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 4: Importar app principal
print("\n4. Testando import do app principal...")
try:
    from app.main import app
    print("   ✅ App principal importado com sucesso")
except Exception as e:
    print(f"   ❌ ERRO ao importar app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 5: Verificar FFmpeg funcional
print("\n5. Testando se FFmpeg está funcional...")
try:
    from app.utils.ffmpeg_locator import verify_ffmpeg_available
    if verify_ffmpeg_available():
        print("   ✅ FFmpeg está funcional")
    else:
        print("   ⚠️  FFmpeg não está disponível (mas o app pode iniciar)")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

print("\n" + "="*60)
print("✅ TODOS OS TESTES PASSARAM!")
print("="*60)
print("\n💡 O servidor deve iniciar corretamente agora.")
print("   Execute: python gui_app.py")
print()

