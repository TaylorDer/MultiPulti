# Настройка GitHub и работа с Git

## Настройка Git (уже выполнено)

Git уже настроен:
- Имя: TaylorDer
- Email: ilya_boyarkin_2004@mail.ru

## Создание репозитория на GitHub

1. Зайдите на https://github.com
2. Нажмите "+" → "New repository"
3. Название: `multipulti` (или другое)
4. Описание: "Мультимедийное веб-пособие по методам оптимизации проектных решений"
5. Выберите Public или Private
6. **НЕ** создавайте README, .gitignore или license (они уже есть)
7. Нажмите "Create repository"

## Привязка к GitHub

После создания репозитория выполните:

```bash
git remote add origin https://github.com/ВАШ_USERNAME/multipulti.git
git branch -M main
git push -u origin main
```

Замените `ВАШ_USERNAME` на ваш GitHub username.

## Работа с коммитами

### Автоматические коммиты
Все изменения автоматически коммитятся при обновлении проекта.

### Ручные коммиты
```bash
git add .
git commit -m "Описание ваших изменений"
git push
```

### Использование скрипта
```powershell
.\auto_commit.ps1 "Ваше сообщение"
```

## Открытие Git Bash

### Способ 1: Через контекстное меню
- Правой кнопкой по папке проекта → "Git Bash Here"

### Способ 2: Через скрипт
```powershell
.\open_bash.ps1
```

### Способ 3: Прямой запуск
```powershell
& "C:\Program Files\Git\bin\bash.exe"
```

## Полезные команды

- `git status` - проверить статус изменений
- `git log` - посмотреть историю коммитов
- `git diff` - посмотреть изменения перед коммитом
- `git pull` - получить изменения с GitHub
- `git push` - отправить изменения на GitHub

