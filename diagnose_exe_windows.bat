@echo off
REM Diagnose script para YouTubeDownloader.exe
REM Coloque este arquivo na mesma pasta do executavel ou execute a partir de onde o exe esteja.

setlocal enabledelayedexpansion

n:: Determinar possiveis locais do exe
set EXE_NAME=YouTubeDownloader.exe
set CAND1=%~dp0%EXE_NAME%
set CAND2=%USERPROFILE%\Desktop\%EXE_NAME%

necho Procurando %EXE_NAME%...
if exist "%~dp0%EXE_NAME%" (
  set EXE_PATH=%~dp0%EXE_NAME%
) else if exist "%USERPROFILE%\Desktop\%EXE_NAME%" (
  set EXE_PATH=%USERPROFILE%\Desktop\%EXE_NAME%
) else (
  echo Nao encontrou %EXE_NAME% em %~dp0 nem na Area de Trabalho.
  echo Copie o exe para esta pasta ou execute o script a partir da pasta do exe.
  pause
  exit /b 1
)

necho Usando: %EXE_PATH%

n:: Pastas de log
set LOG_DIR=%USERPROFILE%\YouTubeDownloader_logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set OUT_LOG=%LOG_DIR%\diagnose_exe_output.txt
set STDERR_LOG=%LOG_DIR%\diagnose_exe_error.txt
set SERVER_LOG=%LOG_DIR%\server.log

necho Logs serao gravados em: %LOG_DIR%

n:: Remover logs antigos (mantem historico se quiser)
ndel /f /q "%OUT_LOG%" >nul 2>&1
ndel /f /q "%STDERR_LOG%" >nul 2>&1

n:: 1) Rodar exe normalmente e capturar stdout/stderr (para ver tracebacks)
necho === Running exe (normal) === > "%OUT_LOG%"
necho (stdout+stderr redirected) >> "%OUT_LOG%"
necho. >> "%OUT_LOG%"
"%EXE_PATH%" >> "%OUT_LOG%" 2>> "%STDERR_LOG%"
necho Exit code: %errorlevel% >> "%OUT_LOG%"
necho. >> "%OUT_LOG%"

n:: 2) Rodar com flag --print-ffmpeg (se suportado)
echo === Running exe --print-ffmpeg === >> "%OUT_LOG%"
"%EXE_PATH%" --print-ffmpeg >> "%OUT_LOG%" 2>> "%STDERR_LOG%"
echo Exit code: %errorlevel% >> "%OUT_LOG%"
echo. >> "%OUT_LOG%"

n:: 3) Rodar com flag --dump-bundle (se suportado)
echo === Running exe --dump-bundle (listing first 200 files) === >> "%OUT_LOG%"
"%EXE_PATH%" --dump-bundle >> "%OUT_LOG%" 2>> "%STDERR_LOG%"
echo Exit code: %errorlevel% >> "%OUT_LOG%"
echo. >> "%OUT_LOG%"

n:: 4) Mostrar server.log (se existir) e o inicio do stderr
necho === server.log (if present) === >> "%OUT_LOG%"
if exist "%SERVER_LOG%" (
  echo server.log encontrado: >> "%OUT_LOG%"
  type "%SERVER_LOG%" >> "%OUT_LOG%"
) else (
  echo server.log nao encontrado em %SERVER_LOG% >> "%OUT_LOG%"
)
necho. >> "%OUT_LOG%"
necho === last 200 lines of stderr === >> "%OUT_LOG%"
if exist "%STDERR_LOG%" (
  powershell -Command "Get-Content -Path '%STDERR_LOG%' -Tail 200 | Out-File -FilePath '%STDERR_LOG%.tail' -Encoding utf8"
  type "%STDERR_LOG%.tail" >> "%OUT_LOG%"
) else (
  echo stderr log nao encontrado >> "%OUT_LOG%"
)
necho. >> "%OUT_LOG%"

n:: Abrir a pasta de logs para o usuario
necho Diagnostico concluido. Abrindo pasta de logs: %LOG_DIR%
explorer "%LOG_DIR%"

n:: Exibir local do arquivo de saida
necho Saida principal: %OUT_LOG%
necho Se quiser, cole o conteudo deste arquivo aqui para analise.
pause
endlocal

