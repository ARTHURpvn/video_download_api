@echo off
REM Script simples para executar a aplicacao

echo Iniciando YouTube Downloader...
echo.

REM Verificar se existe ambiente virtual
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo AVISO: Ambiente virtual nao encontrado!
    echo Execute install_windows.bat primeiro.
    echo.
    pause
    exit /b 1
)

REM Executar aplicacao
python gui_app.py

pause
@echo off
REM ========================================
REM YouTube Downloader - Instalador Completo para Windows
REM Instala Python, FFmpeg e todas as dependências automaticamente
REM ========================================

setlocal enabledelayedexpansion
title YouTube Downloader - Instalador

echo.
echo ========================================
echo   YouTube Downloader - Instalador
echo ========================================
echo.

REM Verificar permissões de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] Este script precisa de permissoes de administrador para instalar FFmpeg.
    echo Por favor, execute como Administrador!
    echo.
    pause
    exit /b 1
)

REM ========================================
REM 1. VERIFICAR E INSTALAR PYTHON
REM ========================================
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Python nao encontrado! Instalando Python 3.11...
    echo.
    echo Baixando Python 3.11.9 (64-bit)...

    REM Baixar Python usando PowerShell
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python-installer.exe'}"

    if exist python-installer.exe (
        echo Instalando Python...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

        REM Aguardar instalacao
        timeout /t 60 /nobreak >nul

        REM Limpar instalador
        del python-installer.exe

        echo Python instalado com sucesso!
        echo.

        REM Recarregar PATH
        call refreshenv.cmd 2>nul
    ) else (
        echo ERRO: Falha ao baixar Python!
        echo Por favor, instale manualmente: https://www.python.org/downloads/
        pause
        exit /b 1
    )
) else (
    echo Python ja instalado!
    python --version
    echo.
)

REM ========================================
REM 2. VERIFICAR E INSTALAR FFMPEG
REM ========================================
echo [2/4] Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo FFmpeg nao encontrado! Instalando...
    echo.

    REM Verificar se chocolatey esta instalado
    choco --version >nul 2>&1
    if %errorLevel% neq 0 (
        echo Instalando Chocolatey (gerenciador de pacotes)...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

        REM Recarregar PATH
        call refreshenv.cmd 2>nul
    )

    echo Instalando FFmpeg via Chocolatey...
    choco install ffmpeg -y

    if %errorLevel% equ 0 (
        echo FFmpeg instalado com sucesso!
        echo.
        call refreshenv.cmd 2>nul
    ) else (
        echo.
        echo [AVISO] Falha na instalacao automatica do FFmpeg.
        echo Tentando metodo alternativo...
        echo.

        REM Metodo alternativo: baixar ffmpeg diretamente
        echo Baixando FFmpeg...
        powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"

        if exist ffmpeg.zip (
            echo Extraindo FFmpeg...
            powershell -Command "Expand-Archive -Path ffmpeg.zip -DestinationPath C:\ffmpeg -Force"

            REM Adicionar ao PATH
            setx /M PATH "%PATH%;C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin"

            del ffmpeg.zip
            echo FFmpeg instalado em C:\ffmpeg
            echo.
        )
    )
) else (
    echo FFmpeg ja instalado!
    ffmpeg -version 2>&1 | findstr "version"
    echo.
)

REM ========================================
REM 3. CRIAR AMBIENTE VIRTUAL E INSTALAR DEPENDENCIAS
REM ========================================
echo [3/4] Configurando ambiente Python...
echo.

REM Criar ambiente virtual se nao existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    echo.
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependencias
echo.
echo Instalando dependencias do projeto...
echo Isso pode levar alguns minutos...
echo.
pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    echo Verifique o arquivo requirements.txt
    pause
    exit /b 1
)

echo.
echo Todas as dependencias instaladas com sucesso!
echo.

REM ========================================
REM 4. VERIFICAR INSTALACAO
REM ========================================
echo [4/4] Verificando instalacao...
echo.

REM Verificar Python
python --version
if %errorLevel% neq 0 (
    echo [ERRO] Python nao esta funcionando corretamente!
    pause
    exit /b 1
)

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo [AVISO] FFmpeg pode nao estar no PATH.
    echo Talvez seja necessario reiniciar o computador.
)

REM Verificar pacotes Python
python -c "import fastapi, uvicorn, yt_dlp, moviepy, tkinter" 2>nul
if %errorLevel% neq 0 (
    echo [ERRO] Alguns pacotes Python nao foram instalados corretamente!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALACAO COMPLETA!
echo ========================================
echo.
echo Tudo foi instalado com sucesso!
echo.
echo Para executar a aplicacao:
echo   1. Execute: run_app.bat
echo   OU
echo   2. Execute: python gui_app.py
echo.
echo Para criar o executavel:
echo   1. Execute: build_executable.bat
echo.
echo ========================================
echo.

REM Perguntar se deseja executar agora
choice /C SN /M "Deseja executar a aplicacao agora"
if errorlevel 2 goto :end
if errorlevel 1 goto :run

:run
echo.
echo Iniciando YouTube Downloader...
python gui_app.py
goto :end

:end
pause

