# Как использовать Bash в Windows

## Вариант 1: Git Bash (рекомендуется)

Git Bash уже установлен вместе с Git. Есть несколько способов его открыть:

### Способ 1: Через меню Пуск
1. Нажмите `Win + S`
2. Введите "Git Bash"
3. Выберите "Git Bash"

### Способ 2: Через контекстное меню
1. Откройте проводник Windows
2. Перейдите в папку проекта
3. Правой кнопкой мыши → "Git Bash Here"

### Способ 3: Через PowerShell скрипт
Выполните в PowerShell:
```powershell
.\open_bash.ps1
```

### Способ 4: Прямой запуск
```powershell
& "C:\Program Files\Git\bin\bash.exe"
```

## Вариант 2: WSL (Windows Subsystem for Linux)

Если у вас установлен WSL:

```powershell
wsl
```

Или конкретный дистрибутив:
```powershell
wsl -d Ubuntu
```

## Вариант 3: Встроенный терминал VS Code

Если используете VS Code:
1. Откройте терминал (`Ctrl + ``)
2. Нажмите на стрелку рядом с `+`
3. Выберите "Git Bash"

## После открытия Bash

Вы окажетесь в bash терминале. Для работы с Git используйте обычные команды:

```bash
git status
git add .
git commit -m "Ваше сообщение"
git push
```

## Настройка Git в Bash

```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш.email@example.com"
```

