# Настройка GitHub для проекта

## Шаг 1: Установка Git

Если Git не установлен, установите его:
- Скачайте с https://git-scm.com/download/win
- Или используйте: `winget install Git.Git`

## Шаг 2: Инициализация репозитория

Выполните в терминале проекта:

```bash
git init
git add .
git commit -m "Initial commit: Мультимедийное веб-пособие по методам оптимизации"
```

## Шаг 3: Создание репозитория на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository" (или "+" → "New repository")
3. Название: `multipulti` (или любое другое)
4. Описание: "Мультимедийное веб-пособие по дисциплине 'Методы оптимизации проектных решений'"
5. Выберите Public или Private
6. НЕ создавайте README, .gitignore или license (они уже есть)
7. Нажмите "Create repository"

## Шаг 4: Привязка к GitHub

После создания репозитория GitHub покажет команды. Выполните:

```bash
git remote add origin https://github.com/ВАШ_USERNAME/multipulti.git
git branch -M main
git push -u origin main
```

Замените `ВАШ_USERNAME` на ваш GitHub username.

## Шаг 5: Последующие коммиты

Для добавления изменений:

```bash
git add .
git commit -m "Описание изменений"
git push
```

## Полезные команды

- `git status` - проверить статус изменений
- `git log` - посмотреть историю коммитов
- `git diff` - посмотреть изменения перед коммитом

