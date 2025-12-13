# Скрипт для открытия Git Bash в текущей директории

$currentDir = Get-Location
$bashPath = "C:\Program Files\Git\bin\bash.exe"

if (Test-Path $bashPath) {
    Write-Host "Открываю Git Bash в директории: $currentDir" -ForegroundColor Green
    Start-Process $bashPath -ArgumentList "--cd=$currentDir"
} else {
    Write-Host "Git Bash не найден по пути: $bashPath" -ForegroundColor Red
    Write-Host "Попробуйте найти Git Bash вручную или используйте WSL" -ForegroundColor Yellow
}

