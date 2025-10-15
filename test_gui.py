#!/usr/bin/env python3
"""
Script de teste para verificar se a GUI está funcionando corretamente
"""

import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("TESTE DE INICIALIZAÇÃO DA GUI")
print("=" * 60)

try:
    print("\n1. Verificando imports...")
    import tkinter as tk
    from tkinter import ttk, messagebox
    print("   ✓ Tkinter importado com sucesso")

    import requests
    print("   ✓ Requests importado com sucesso")

    from pathlib import Path
    print("   ✓ Path importado com sucesso")

    print("\n2. Verificando estrutura do projeto...")
    if os.path.exists('app'):
        print("   ✓ Diretório 'app' encontrado")
    else:
        print("   ✗ Diretório 'app' NÃO encontrado")

    if os.path.exists('app/routes'):
        print("   ✓ Diretório 'app/routes' encontrado")
    else:
        print("   ✗ Diretório 'app/routes' NÃO encontrado")

    print("\n3. Testando importação da GUI...")
    from gui_app import YouTubeDownloaderGUI, DOWNLOAD_DIR
    print(f"   ✓ GUI importada com sucesso")
    print(f"   ✓ Diretório de downloads: {DOWNLOAD_DIR}")

    print("\n4. Criando janela de teste...")
    root = tk.Tk()
    root.withdraw()  # Esconder janela
    print("   ✓ Janela Tkinter criada")

    print("\n5. Inicializando aplicação...")
    app = YouTubeDownloaderGUI(root)
    print("   ✓ Aplicação inicializada")

    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print("\nA GUI está pronta para uso.")
    print("Execute: python gui_app.py")
    print("=" * 60)

    root.destroy()

except Exception as e:
    print("\n" + "=" * 60)
    print("❌ ERRO ENCONTRADO:")
    print("=" * 60)
    print(f"\n{type(e).__name__}: {str(e)}")
    import traceback
    print("\nTraceback completo:")
    traceback.print_exc()
    print("=" * 60)
    sys.exit(1)

