#!/bin/bash
###############################################################################
# YouTube Downloader - Instalador Automático macOS
# Este script instala tudo automaticamente, incluindo Python se necessário
###############################################################################

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear
echo ""
echo "========================================================================"
echo "              YOUTUBE DOWNLOADER - INSTALADOR MACOS"
echo "========================================================================"
echo ""
echo " Este instalador vai:"
echo "   [1] Verificar/Instalar Python automaticamente"
echo "   [2] Instalar todas as dependências"
echo "   [3] Criar o aplicativo na sua Área de Trabalho"
echo ""
echo " Tempo estimado: 10-15 minutos"
echo ""
echo "========================================================================"
echo ""
read -p "Pressione ENTER para continuar..."

echo ""
echo -e "${BLUE}[ETAPA 1/6] Verificando Python...${NC}"
echo ""

# Verificar se Python3 está instalado
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}[OK] Python encontrado: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
else
    echo -e "${YELLOW}[AVISO] Python3 não encontrado!${NC}"
    echo ""
    echo "Opções:"
    echo "  1. Instalar Python via Homebrew (recomendado)"
    echo "  2. Sair e instalar manualmente"
    echo ""
    read -p "Escolha uma opção (1 ou 2): " choice

    case $choice in
        1)
            echo ""
            echo -e "${BLUE}[INSTALANDO PYTHON...]${NC}"

            # Verificar se Homebrew está instalado
            if ! command -v brew &> /dev/null; then
                echo "Homebrew não encontrado. Instalando Homebrew primeiro..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

                # Adicionar Homebrew ao PATH
                echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
                eval "$(/opt/homebrew/bin/brew shellenv)"
            fi

            echo "Instalando Python3..."
            brew install python3

            if command -v python3 &> /dev/null; then
                echo -e "${GREEN}[OK] Python instalado com sucesso!${NC}"
                PYTHON_CMD="python3"
            else
                echo -e "${RED}[ERRO] Falha ao instalar Python!${NC}"
                echo "Por favor, instale manualmente: https://www.python.org/downloads/"
                exit 1
            fi
            ;;
        2)
            echo ""
            echo "Por favor, instale o Python manualmente:"
            echo "  1. Acesse: https://www.python.org/downloads/"
            echo "  2. Baixe a versão mais recente para macOS"
            echo "  3. Execute este instalador novamente"
            echo ""
            exit 1
            ;;
        *)
            echo "Opção inválida!"
            exit 1
            ;;
    esac
fi

# Navegar para o diretório do projeto
cd "$(dirname "$0")"

echo ""
echo -e "${BLUE}[ETAPA 2/6] Atualizando pip...${NC}"
$PYTHON_CMD -m pip install --upgrade pip --quiet

echo ""
echo -e "${BLUE}[ETAPA 3/6] Instalando dependências...${NC}"
echo "(Isso pode levar alguns minutos)"
echo ""

$PYTHON_CMD -m pip install yt-dlp --quiet
echo -e "${GREEN} [OK] yt-dlp instalado${NC}"

$PYTHON_CMD -m pip install fastapi --quiet
echo -e "${GREEN} [OK] fastapi instalado${NC}"

$PYTHON_CMD -m pip install "uvicorn[standard]" --quiet
echo -e "${GREEN} [OK] uvicorn instalado${NC}"

$PYTHON_CMD -m pip install python-multipart --quiet
echo -e "${GREEN} [OK] python-multipart instalado${NC}"

$PYTHON_CMD -m pip install requests --quiet
echo -e "${GREEN} [OK] requests instalado${NC}"

$PYTHON_CMD -m pip install pydantic --quiet
echo -e "${GREEN} [OK] pydantic instalado${NC}"

$PYTHON_CMD -m pip install pyinstaller --quiet
echo -e "${GREEN} [OK] pyinstaller instalado${NC}"

echo ""
echo -e "${BLUE}[ETAPA 4/6] Verificando FFmpeg...${NC}"
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}[OK] FFmpeg já instalado${NC}"
else
    echo -e "${YELLOW}[AVISO] FFmpeg não encontrado${NC}"
    echo "Instalando FFmpeg via Homebrew..."

    if command -v brew &> /dev/null; then
        brew install ffmpeg
        echo -e "${GREEN}[OK] FFmpeg instalado${NC}"
    else
        echo -e "${YELLOW}[AVISO] Homebrew não encontrado. FFmpeg será baixado quando necessário.${NC}"
    fi
fi

echo ""
echo -e "${BLUE}[ETAPA 5/6] Criando pasta de downloads...${NC}"
DOWNLOAD_DIR="$HOME/Downloads/Videos Baixados"
mkdir -p "$DOWNLOAD_DIR"
echo -e "${GREEN}[OK] Pasta criada: $DOWNLOAD_DIR${NC}"

echo ""
echo -e "${BLUE}[ETAPA 6/6] Compilando aplicativo...${NC}"
echo -e "${YELLOW}(AGUARDE: Isso pode levar 10-15 minutos!)${NC}"
echo ""

$PYTHON_CMD build_executable.py

APP_PATH="$HOME/Desktop/YouTubeDownloader"

if [ -f "$APP_PATH" ]; then
    # Tornar executável
    chmod +x "$APP_PATH"

    echo ""
    echo "========================================================================"
    echo "               INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "========================================================================"
    echo ""
    echo -e "${GREEN} [OK] Aplicativo criado em: $APP_PATH${NC}"
    echo ""
    echo " Como usar:"
    echo "   1. Vá até sua Área de Trabalho"
    echo "   2. Duplo clique em 'YouTubeDownloader'"
    echo "   3. Cole um link do YouTube"
    echo "   4. Clique em 'BAIXAR AGORA'"
    echo ""
    echo " Vídeos serão salvos em: $DOWNLOAD_DIR"
    echo ""
    echo "========================================================================"
    echo ""

    # Perguntar se quer abrir o aplicativo
    read -p "Deseja abrir o aplicativo agora? (s/N): " open_app
    case $open_app in
        [sS]|[sS][iI][mM])
            open "$APP_PATH"
            ;;
    esac
else
    echo ""
    echo -e "${RED}[ERRO] Falha ao criar aplicativo!${NC}"
    echo "Tente executar manualmente: python3 gui_app.py"
fi

echo ""
read -p "Pressione ENTER para sair..."

# ============================================================================
# YouTube Downloader - Instalador Automático Windows
# Este script instala tudo automaticamente, incluindo Python se necessário
# ============================================================================

title YouTube Downloader - Instalador
color 0A
cls

echo.
echo ========================================================================
echo                    YOUTUBE DOWNLOADER - INSTALADOR
echo ========================================================================
echo.
echo  Este instalador vai:
echo    [1] Verificar/Instalar Python automaticamente
echo    [2] Instalar todas as dependencias
echo    [3] Criar o executavel na sua Area de Trabalho
echo.
echo  Tempo estimado: 10-15 minutos
echo.
echo ========================================================================
echo.
pause

echo.
echo [ETAPA 1/5] Verificando Python...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python encontrado!
    python --version
    goto :install_deps
)

echo [AVISO] Python nao encontrado!
echo.
echo Opcoes:
echo  1. Instalar Python automaticamente (recomendado^)
echo  2. Sair e instalar manualmente
echo.
choice /C 12 /N /M "Escolha uma opcao (1 ou 2): "

if errorlevel 2 goto :manual_install
if errorlevel 1 goto :auto_install

:auto_install
echo.
echo [INSTALANDO PYTHON...]
echo Baixando Python 3.11...
echo.

REM Criar pasta temporária
if not exist "%TEMP%\ytdownloader" mkdir "%TEMP%\ytdownloader"
cd /d "%TEMP%\ytdownloader"

REM Baixar Python installer
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python-installer.exe'}"

if not exist "python-installer.exe" (
    echo.
    echo [ERRO] Falha ao baixar Python!
    echo Por favor, instale manualmente: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Instalando Python (aguarde...)
echo IMPORTANTE: Python sera instalado automaticamente com ADD TO PATH
echo.

REM Instalar Python silenciosamente com PATH
start /wait python-installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

REM Atualizar PATH na sessão atual
call refreshenv >nul 2>&1
set PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%

echo.
echo [OK] Python instalado com sucesso!
timeout /t 2 >nul

:install_deps
echo.
echo [ETAPA 2/5] Atualizando pip...
python -m pip install --upgrade pip --quiet

echo.
echo [ETAPA 3/5] Instalando dependencias...
echo (Isso pode levar alguns minutos)
echo.

cd /d "%~dp0.."

python -m pip install yt-dlp --quiet
echo  [OK] yt-dlp instalado

python -m pip install fastapi --quiet
echo  [OK] fastapi instalado

python -m pip install "uvicorn[standard]" --quiet
echo  [OK] uvicorn instalado

python -m pip install python-multipart --quiet
echo  [OK] python-multipart instalado

python -m pip install requests --quiet
echo  [OK] requests instalado

python -m pip install pydantic --quiet
echo  [OK] pydantic instalado

python -m pip install pyinstaller --quiet
echo  [OK] pyinstaller instalado

echo.
echo [ETAPA 4/5] Criando pasta de downloads...
set DOWNLOAD_DIR=%USERPROFILE%\Downloads\Videos Baixados
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"
echo  [OK] Pasta criada: %DOWNLOAD_DIR%

echo.
echo [ETAPA 5/5] Compilando executavel...
echo (AGUARDE: Isso pode levar 10-15 minutos!)
echo.

python build_executable.py

if exist "%USERPROFILE%\Desktop\YouTubeDownloader.exe" (
    echo.
    echo ========================================================================
    echo                     INSTALACAO CONCLUIDA COM SUCESSO!
    echo ========================================================================
    echo.
    echo  [OK] Executavel criado em: %USERPROFILE%\Desktop\YouTubeDownloader.exe
    echo.
    echo  Como usar:
    echo    1. Va ate sua Area de Trabalho
    echo    2. Duplo clique em "YouTubeDownloader.exe"
    echo    3. Cole um link do YouTube
    echo    4. Clique em "BAIXAR AGORA"
    echo.
    echo  Videos serao salvos em: %DOWNLOAD_DIR%
    echo.
    echo ========================================================================
    echo.

    REM Perguntar se quer abrir o aplicativo
    choice /C SN /N /M "Deseja abrir o aplicativo agora? (S/N): "
    if errorlevel 2 goto :end
    if errorlevel 1 (
        start "" "%USERPROFILE%\Desktop\YouTubeDownloader.exe"
        timeout /t 2 >nul
        exit
    )
) else (
    echo.
    echo [ERRO] Falha ao criar executavel!
    echo Tente executar manualmente: python gui_app.py
)

goto :end

:manual_install
echo.
echo Por favor, instale o Python manualmente:
echo  1. Acesse: https://www.python.org/downloads/
echo  2. Baixe a versao mais recente
echo  3. IMPORTANTE: Marque "Add Python to PATH" durante instalacao
echo  4. Execute este instalador novamente
echo.
pause
exit /b 1

:end
echo.
pause

# Script de Instalação Automática - YouTube Downloader (macOS)
# Este script instala todas as dependências necessárias, incluindo o FFmpeg

echo "=============================================="
echo "🚀 YouTube Downloader - Instalação Automática"
echo "=============================================="
echo ""

# Verificar se está no macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script é apenas para macOS!"
    echo "   Use INSTALAR_WINDOWS.bat no Windows"
    exit 1
fi

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Verificar/Instalar Homebrew
echo "📦 Verificando Homebrew..."
if ! command_exists brew; then
    echo "   ⚠️  Homebrew não encontrado. Instalando..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Adicionar Homebrew ao PATH
    if [[ -d "/opt/homebrew/bin" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    echo "   ✅ Homebrew instalado!"
else
    echo "   ✅ Homebrew já instalado"
fi

# 2. Atualizar Homebrew
echo ""
echo "🔄 Atualizando Homebrew..."
brew update

# 3. Instalar Python 3 (se necessário)
echo ""
echo "🐍 Verificando Python 3..."
if ! command_exists python3; then
    echo "   ⚠️  Python 3 não encontrado. Instalando..."
    brew install python@3.11
    echo "   ✅ Python 3 instalado!"
else
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ Python já instalado: $PYTHON_VERSION"
fi

# 4. INSTALAR FFMPEG (CRÍTICO!)
echo ""
echo "🎬 Instalando FFmpeg..."
if ! command_exists ffmpeg; then
    echo "   ⚠️  FFmpeg não encontrado. Instalando..."
    brew install ffmpeg
    echo "   ✅ FFmpeg instalado com sucesso!"
else
    echo "   ✅ FFmpeg já instalado"
    FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
    echo "   📍 $FFMPEG_VERSION"

    # Verificar se precisa atualizar
    echo "   🔄 Verificando atualizações do FFmpeg..."
    brew upgrade ffmpeg 2>/dev/null || echo "   ✅ FFmpeg já está na versão mais recente"
fi

# Verificar localização do FFmpeg
FFMPEG_PATH=$(which ffmpeg)
echo "   📍 FFmpeg instalado em: $FFMPEG_PATH"

# 5. Criar ambiente virtual Python
echo ""
echo "📁 Criando ambiente virtual Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Ambiente virtual criado"
else
    echo "   ✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
source venv/bin/activate

# 6. Atualizar pip
echo ""
echo "⬆️  Atualizando pip..."
python -m pip install --upgrade pip

# 7. Instalar dependências Python
echo ""
echo "📚 Instalando dependências Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "   ✅ Dependências instaladas!"
else
    echo "   ⚠️  requirements.txt não encontrado. Instalando dependências básicas..."
    pip install fastapi uvicorn yt-dlp requests pydantic python-multipart
fi

# 8. Atualizar yt-dlp para versão mais recente
echo ""
echo "🔄 Atualizando yt-dlp para versão mais recente..."
pip install --upgrade yt-dlp

# 9. Instalar PyInstaller (para criar executável)
echo ""
echo "📦 Instalando PyInstaller..."
pip install pyinstaller

# 10. Verificação final
echo ""
echo "=============================================="
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "=============================================="
echo ""
echo "📋 Resumo da instalação:"
echo "   ✅ Homebrew: $(brew --version | head -n 1)"
echo "   ✅ Python: $(python --version)"
echo "   ✅ FFmpeg: $(ffmpeg -version | head -n 1 | cut -d' ' -f3)"
echo "   ✅ yt-dlp: $(yt-dlp --version)"
echo "   ✅ PyInstaller: $(pyinstaller --version)"
echo ""
echo "🎯 Próximos passos:"
echo "   1. Para USAR o aplicativo:"
echo "      python3 gui_app.py"
echo ""
echo "   2. Para COMPILAR o executável:"
echo "      python3 build_executable.py"
echo "      ou"
echo "      pyinstaller YouTubeDownloader.spec --clean"
echo ""
echo "   3. O executável estará em: dist/YouTubeDownloader.app"
echo ""
echo "💡 Dica: O FFmpeg foi instalado em: $FFMPEG_PATH"
echo "   Ele será automaticamente incluído no executável."
echo ""

# Manter terminal aberto
read -p "Pressione ENTER para fechar..."
