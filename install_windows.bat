@echo off
title YouTube Downloader - Instalador
color 0C

echo ============================================
echo  YouTube Downloader - Instalador Automatico
echo ============================================
echo.

REM Verificar se Python esta instalado
echo Verificando instalacao do Python...
python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [AVISO] Python nao encontrado!
    echo.
    echo Deseja baixar e instalar o Python automaticamente?
    echo.
    choice /C SN /M "Instalar Python agora? (S=Sim, N=Nao)"

    if errorlevel 2 (
        echo.
        echo Instalacao cancelada.
        echo Por favor, instale o Python manualmente:
        echo https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Baixando Python...
    echo Por favor, aguarde...

    REM Criar diretorio temporario
    if not exist "%TEMP%\youtube_downloader" mkdir "%TEMP%\youtube_downloader"

    REM Baixar Python (versao 3.11.9 - estavel e compativel)
    powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\youtube_downloader\python_installer.exe'}"

    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao baixar o Python.
        echo Por favor, instale manualmente de:
        echo https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Instalando Python...
    echo IMPORTANTE: Aguarde a instalacao completa!
    echo.

    REM Instalar Python silenciosamente com pip e add to PATH
    "%TEMP%\youtube_downloader\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    if errorlevel 1 (
        echo.
        echo ERRO: Falha na instalacao do Python.
        echo Tente instalar manualmente de:
        echo https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )

    echo.
    echo Python instalado com sucesso!
    echo.

    REM Limpar arquivo temporario
    del "%TEMP%\youtube_downloader\python_installer.exe" >nul 2>&1

    REM Atualizar PATH para a sessao atual
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts"

    echo Verificando instalacao...
    timeout /t 3 /nobreak >nul

    python --version

    if errorlevel 1 (
        echo.
        echo AVISO: Python instalado, mas pode ser necessario reiniciar o computador.
        echo Por favor, reinicie e execute este instalador novamente.
        echo.
        pause
        exit /b 1
    )
) else (
    echo Python encontrado!
    python --version
)

echo.
echo Este instalador ira:
echo  - Verificar Python [OK]
echo  - Instalar todas as dependencias
echo  - Configurar o FFmpeg
echo  - Preparar o aplicativo
echo.
echo Pressione qualquer tecla para continuar...
pause > nul

cls
echo Iniciando instalador de dependencias...
echo.

python install_windows.py

if errorlevel 1 (
    echo.
    echo ERRO: Nao foi possivel executar o instalador.
    echo.
    pause
    exit /b 1
)

echo.
echo Instalacao concluida com sucesso!
pause
