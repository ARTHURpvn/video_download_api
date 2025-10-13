@echo off
REM Script para build no Windows - COMPLETO COM INSTALACAO DE DEPENDENCIAS

echo ========================================
echo YouTube Downloader - Build Script
echo ========================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Execute install_windows.bat primeiro para instalar todas as dependencias.
    echo.
    pause
    exit /b 1
)

echo Python encontrado:
python --version
echo.

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] FFmpeg nao encontrado!
    echo O executavel funcionara, mas FFmpeg precisa estar instalado no sistema de destino.
    echo.
    echo Execute install_windows.bat para instalar FFmpeg automaticamente.
    echo.
    choice /C SN /M "Deseja continuar mesmo assim"
    if errorlevel 2 exit /b 1
    echo.
)

REM Criar/ativar ambiente virtual
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    echo.
)

echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar/atualizar dependencias
echo.
echo Verificando dependencias...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo.
echo Verificando PyInstaller...
pip install pyinstaller --quiet

REM Executar build
echo.
echo ========================================
echo Construindo executavel...
echo ========================================
echo.
python build_executable.py

if %errorLevel% equ 0 (
    echo.
    echo ========================================
    echo BUILD COMPLETO COM SUCESSO!
    echo ========================================
    echo.
    echo Executavel criado em: dist\YouTubeDownloader.exe
    echo.
    echo Voce pode:
    echo   1. Executar: dist\YouTubeDownloader.exe
    echo   2. Mover o arquivo para qualquer lugar
    echo   3. Compartilhar com outros (FFmpeg precisa estar instalado)
    echo.
    echo ========================================
) else (
    echo.
    echo [ERRO] Falha no build!
    echo.
)

echo.
pause
