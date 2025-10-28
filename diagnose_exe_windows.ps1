# Diagnose script PowerShell para YouTubeDownloader.exe
# Execute este script no PowerShell (recomendado como administrador se necessario).
param(
    [string]$ExePath = "$env:USERPROFILE\Desktop\YouTubeDownloader.exe"
)

nif (-not (Test-Path $ExePath)) {
    Write-Host "Executavel nao encontrado em: $ExePath" -ForegroundColor Red
    exit 1
}

n$logDir = "$env:USERPROFILE\YouTubeDownloader_logs"
if (-not (Test-Path $logDir)) { New-Item -Path $logDir -ItemType Directory | Out-Null }
$outLog = Join-Path $logDir "diagnose_exe_output.txt"
$errLog = Join-Path $logDir "diagnose_exe_error.txt"
$serverLog = Join-Path $logDir "server.log"

if (Test-Path $outLog) { Remove-Item $outLog -Force }
if (Test-Path $errLog) { Remove-Item $errLog -Force }

Write-Host "Running: $ExePath"

# Run normally and capture output
Write-Host "-> Running exe (normal)"
Start-Process -FilePath $ExePath -NoNewWindow -RedirectStandardOutput $outLog -RedirectStandardError $errLog -Wait
Write-Host "Exit code capture complete"

# Run with --print-ffmpeg
Write-Host "-> Running with --print-ffmpeg"
& $ExePath --print-ffmpeg *>> $outLog 2>> $errLog

# Run with --dump-bundle (may be large)
Write-Host "-> Running with --dump-bundle"
& $ExePath --dump-bundle *>> $outLog 2>> $errLog

# Append server.log if exists
Write-Host "-> Appending server.log (if present)"
if (Test-Path $serverLog) { Get-Content $serverLog | Out-File -FilePath $outLog -Append }

Write-Host "Diagnostico concluido. Logs em: $logDir"
Invoke-Item $logDir
Write-Host "Cole o arquivo diagnose_exe_output.txt aqui para analise"
Read-Host -Prompt 'Pressione Enter para sair'

