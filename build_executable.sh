#!/bin/bash
# Script para build no macOS/Linux

echo "🚀 YouTube Downloader - Build Script"
echo "===================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar/ativar ambiente virtual
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

echo "🔄 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Executar build
echo ""
echo "🔨 Construindo executável..."
python build_executable.py

echo ""
echo "✅ Processo concluído!"
echo ""
echo "Para executar o app localmente:"
echo "  python gui_app.py"
echo ""
echo "Para usar o executável:"
echo "  ./dist/YouTubeDownloader"

