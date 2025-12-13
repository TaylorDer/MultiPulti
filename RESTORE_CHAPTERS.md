# Инструкция по восстановлению chapters.ts

## Проблема
Файл `src/data/chapters.ts` был перезаписан и теперь содержит только минимальную структуру.

## Решение

### Вариант 1: Восстановление из Git (рекомендуется)
Если у вас есть git репозиторий:

```bash
git checkout HEAD -- src/data/chapters.ts
```

Или если файл был изменен недавно:

```bash
git log --oneline src/data/chapters.ts
git checkout <commit-hash> -- src/data/chapters.ts
```

### Вариант 2: Ручное восстановление
Если у вас есть резервная копия файла, скопируйте её в `src/data/chapters.ts`

### После восстановления

1. Убедитесь, что оригинальный `chapters.ts` содержит все секции с полем `content:`
2. Запустите скрипт для извлечения:

```bash
python extract_sections_final.py
```

Скрипт:
- Создаст все `.md` файлы в `src/content/chapters/`
- Обновит `chapters.ts` с только метаданными (id, title, markdownFile)
- Создаст резервную копию оригинального файла в `src/data/chapters.ts.backup`

## Проверка

После выполнения скрипта:
1. Проверьте, что все `.md` файлы созданы в `src/content/chapters/`
2. Проверьте, что `chapters.ts` содержит только метаданные (без длинных строк content)
3. Запустите проект: `npm run dev`
4. Убедитесь, что все секции загружаются корректно


