@echo off
REM ============================================================================
REM YouTube Downloader - Instalador Automático Windows
REM Este script instala tudo automaticamente, incluindo Python se necessário
REM ============================================================================

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
echo  1. Instalar Python automaticamente (recomendado)
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

cd /d "%~dp0"

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

