# Скрипт для автоматического коммита изменений

$env:Path += ";C:\Program Files\Git\cmd"

# Проверяем настройки Git
$userName = git config --global user.name 2>$null
$userEmail = git config --global user.email 2>$null

if (-not $userName -or -not $userEmail) {
    Write-Host "Git не настроен. Настройте имя и email:" -ForegroundColor Yellow
    Write-Host "git config --global user.name `"Ваше Имя`"" -ForegroundColor Cyan
    Write-Host "git config --global user.email `"ваш.email@example.com`"" -ForegroundColor Cyan
    exit 1
}

# Получаем статус
$status = git status --porcelain

if (-not $status) {
    Write-Host "Нет изменений для коммита" -ForegroundColor Gray
    exit 0
}

# Добавляем все изменения
git add .

# Получаем сообщение коммита из аргумента или используем дефолтное
$commitMessage = $args[0]
if (-not $commitMessage) {
    $commitMessage = "Update: автоматическое обновление проекта"
}

# Создаем коммит
git commit -m $commitMessage

Write-Host "✓ Коммит создан: $commitMessage" -ForegroundColor Green

# Показываем статус
git status --short


