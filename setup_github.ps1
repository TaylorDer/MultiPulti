# Скрипт для настройки GitHub репозитория

# Добавляем Git в PATH
$env:Path += ";C:\Program Files\Git\cmd"

Write-Host "=== Настройка GitHub репозитория ===" -ForegroundColor Green
Write-Host ""

# Проверяем, что Git доступен
try {
    $gitVersion = git --version
    Write-Host "✓ Git установлен: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Git не найден. Установите Git сначала." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Шаг 1: Добавление файлов в staging..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "Шаг 2: Создание первого коммита..." -ForegroundColor Yellow
git commit -m "Initial commit: Мультимедийное веб-пособие по методам оптимизации проектных решений"

Write-Host ""
Write-Host "✓ Первый коммит создан!" -ForegroundColor Green
Write-Host ""
Write-Host "=== Следующие шаги ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Создайте репозиторий на GitHub:"
Write-Host "   https://github.com/new" -ForegroundColor Blue
Write-Host ""
Write-Host "2. После создания репозитория выполните:"
Write-Host "   git remote add origin https://github.com/ВАШ_USERNAME/НАЗВАНИЕ_РЕПО.git" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Замените ВАШ_USERNAME и НАЗВАНИЕ_РЕПО на ваши значения." -ForegroundColor Gray
Write-Host ""


