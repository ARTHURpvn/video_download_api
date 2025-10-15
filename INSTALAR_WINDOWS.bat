@echo off
REM ============================================================================
REM YouTube Downloader - Instalador Automático Windows
REM Este script instala tudo automaticamente, incluindo Python e FFmpeg
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
echo    [2] Verificar/Instalar FFmpeg automaticamente
echo    [3] Instalar todas as dependencias
echo    [4] Criar o executavel na sua Area de Trabalho
echo.
echo  Tempo estimado: 10-15 minutos
echo.
echo ========================================================================
echo.
pause

echo.
echo [ETAPA 1/6] Verificando Python...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python encontrado!
    python --version
    goto :check_ffmpeg
) else (
    echo [AVISO] Python nao encontrado!
    echo.
    echo Opcoes:
    echo  1. Instalar Python automaticamente (recomendado)
    echo  2. Sair e instalar manualmente
    echo.
    choice /C 12 /N /M "Escolha uma opcao (1 ou 2): "

    if errorlevel 2 goto :manual_install_python
    if errorlevel 1 goto :auto_install_python
)

:auto_install_python
echo.
echo [INSTALANDO PYTHON...]
echo Baixando Python 3.11...
echo.

REM Criar pasta temporária
if not exist "%TEMP%\ytdownloader" mkdir "%TEMP%\ytdownloader"
cd /d "%TEMP%\ytdownloader"

REM Baixar Python installer
powershell -Command "Write-Host 'Baixando Python...' -ForegroundColor Yellow; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python-installer.exe' -UseBasicParsing"

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
set PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%

echo.
echo [OK] Python instalado com sucesso!
timeout /t 2 >nul

REM Voltar para diretório do projeto
cd /d "%~dp0"

:check_ffmpeg
echo.
echo [ETAPA 2/6] Verificando FFmpeg...
echo.

REM Verificar se FFmpeg já está instalado
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] FFmpeg ja instalado!
    for /f "tokens=*" %%i in ('where ffmpeg') do set FFMPEG_PATH=%%i
    echo [OK] FFmpeg encontrado em: %FFMPEG_PATH%
    goto :install_deps
)

echo [AVISO] FFmpeg nao encontrado. Instalando automaticamente...
echo.

REM Criar pasta para FFmpeg
set FFMPEG_DIR=%LOCALAPPDATA%\FFmpeg
if not exist "%FFMPEG_DIR%" mkdir "%FFMPEG_DIR%"

REM Baixar FFmpeg (versão essentials)
echo Baixando FFmpeg (pode levar alguns minutos)...
cd /d "%TEMP%\ytdownloader"

powershell -Command "Write-Host 'Baixando FFmpeg...' -ForegroundColor Yellow; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip' -UseBasicParsing"

if not exist "ffmpeg.zip" (
    echo.
    echo [ERRO] Falha ao baixar FFmpeg!
    echo.
    echo Por favor, baixe manualmente:
    echo 1. Acesse: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Baixe "ffmpeg-release-essentials.zip"
    echo 3. Extraia em C:\ffmpeg
    echo 4. Adicione C:\ffmpeg\bin ao PATH
    echo.
    pause
    goto :install_deps
)

echo.
echo Extraindo FFmpeg...
powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '%TEMP%\ytdownloader\ffmpeg_extracted' -Force"

REM Encontrar a pasta extraída (nome varia com versão)
for /d %%i in ("%TEMP%\ytdownloader\ffmpeg_extracted\ffmpeg-*") do set EXTRACTED_DIR=%%i

if not exist "%EXTRACTED_DIR%\bin\ffmpeg.exe" (
    echo [ERRO] Erro ao extrair FFmpeg!
    goto :install_deps
)

echo Instalando FFmpeg em: %FFMPEG_DIR%
xcopy "%EXTRACTED_DIR%\bin\*" "%FFMPEG_DIR%\" /E /I /Y >nul

REM Adicionar FFmpeg ao PATH do usuário permanentemente
echo Adicionando FFmpeg ao PATH...
powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%FFMPEG_DIR%', 'User')"

REM Adicionar ao PATH da sessão atual
set PATH=%PATH%;%FFMPEG_DIR%

REM Verificar se funcionou
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo [OK] FFmpeg instalado com sucesso em: %FFMPEG_DIR%
    echo [OK] FFmpeg adicionado ao PATH do sistema
) else (
    echo.
    echo [AVISO] FFmpeg instalado mas pode precisar reiniciar o terminal
    echo         Caminho: %FFMPEG_DIR%
)

REM Limpar arquivos temporários
del /f /q "%TEMP%\ytdownloader\ffmpeg.zip" >nul 2>&1
rd /s /q "%TEMP%\ytdownloader\ffmpeg_extracted" >nul 2>&1

REM Voltar para diretório do projeto
cd /d "%~dp0"

:install_deps
echo.
echo [ETAPA 3/6] Atualizando pip...
python -m pip install --upgrade pip --quiet

echo.
echo [ETAPA 4/6] Instalando dependencias Python...
echo (Isso pode levar alguns minutos)
echo.

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
echo [ETAPA 5/6] Criando pasta de downloads...
set DOWNLOAD_DIR=%USERPROFILE%\Downloads\Videos Baixados
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"
echo  [OK] Pasta criada: %DOWNLOAD_DIR%

echo.
echo [ETAPA 6/6] Compilando executavel...
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

:manual_install_python
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
echo ========================================================================
echo                           RESUMO DA INSTALACAO
echo ========================================================================
echo.
python --version 2>nul
echo.
ffmpeg -version 2>nul | findstr "ffmpeg version"
echo.
yt-dlp --version 2>nul | findstr /v "^$"
echo.
echo ========================================================================
echo.
pause
