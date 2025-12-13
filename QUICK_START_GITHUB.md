# Быстрая настройка GitHub

## Шаг 1: Настройка Git (выполните один раз)

Настройте ваше имя и email для Git:

```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш.email@example.com"
```

Например:
```bash
git config --global user.name "Ilya"
git config --global user.email "ilya@example.com"
```

## Шаг 2: Создание первого коммита

После настройки имени и email выполните:

```bash
git add .
git commit -m "Initial commit: Мультимедийное веб-пособие по методам оптимизации"
```

## Шаг 3: Создание репозитория на GitHub

1. Зайдите на https://github.com
2. Нажмите "+" → "New repository"
3. Название: `multipulti` (или другое)
4. Описание: "Мультимедийное веб-пособие по методам оптимизации проектных решений"
5. Выберите Public или Private
6. **НЕ** создавайте README, .gitignore или license (они уже есть)
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
git commit -m "Описание ваших изменений"
git push
```

## Полезные команды

- `git status` - проверить статус изменений
- `git log` - посмотреть историю коммитов
- `git diff` - посмотреть изменения перед коммитом
- `git pull` - получить изменения с GitHub

