#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для извлечения content из chapters.ts в отдельные .md файлы
Использует простой подход: парсит весь файл как строку и находит секции
"""

import re
import os

# Сначала проверим, есть ли оригинальный файл
if not os.path.exists('src/data/chapters.ts'):
    print("ОШИБКА: chapters.ts не найден!")
    exit(1)

file_size = os.path.getsize('src/data/chapters.ts')
if file_size < 1000:
    print("ПРЕДУПРЕЖДЕНИЕ: chapters.ts очень маленький (меньше 1KB)")
    print("Возможно, файл был перезаписан. Нужно восстановить оригинальный файл.")
    print("См. инструкцию в RESTORE_CHAPTERS.md")
    response = input("Продолжить? (y/n): ")
    if response.lower() != 'y':
        exit(1)

# Читаем весь файл
with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Создаем директорию для markdown файлов
os.makedirs('src/content/chapters', exist_ok=True)

# Проверяем, есть ли уже markdownFile вместо content
if 'markdownFile:' in full_text and 'content:' not in full_text:
    print("Файл уже содержит markdownFile. Возможно, он уже был обработан.")
    response = input("Продолжить? (y/n): ")
    if response.lower() != 'y':
        exit(1)

# Находим все главы и их структуру
chapters_data = []

# Ищем все главы по паттерну
# Разбиваем на главы - ищем начало новой главы
chapter_pattern = r"\{\s*id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*sections:\s*\["
chapter_matches = list(re.finditer(chapter_pattern, full_text))

if not chapter_matches:
    print("ОШИБКА: Не найдено глав в файле!")
    print("Убедитесь, что файл содержит структуру chapters с id, title, sections")
    exit(1)

print(f"Найдено глав: {len(chapter_matches)}")

# Обрабатываем каждую главу
for i, chapter_match in enumerate(chapter_matches):
    chapter_id = chapter_match.group(1)
    chapter_title = chapter_match.group(2)
    chapter_start = chapter_match.start()
    
    # Находим конец этой главы
    if i + 1 < len(chapter_matches):
        chapter_end = chapter_matches[i + 1].start()
    else:
        # Последняя глава - ищем закрывающую скобку массива chapters
        chapter_end = full_text.find('];', chapter_start)
        if chapter_end == -1:
            chapter_end = len(full_text)
    
    chapter_block = full_text[chapter_start:chapter_end]
    
    # Находим все секции в этой главе
    sections = []
    
    # Ищем секции по паттерну: id, title, content
    section_pattern = r"\{\s*id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*content:\s*`"
    
    for section_match in re.finditer(section_pattern, chapter_block):
        section_id = section_match.group(1)
        section_title = section_match.group(2)
        content_start = section_match.end()
        
        # Находим конец content - ищем закрывающую обратную кавычку
        # Нужно учесть, что внутри могут быть экранированные обратные кавычки
        content_end = content_start
        i = content_start
        found_end = False
        
        while i < len(chapter_block):
            if chapter_block[i] == '\\' and i + 1 < len(chapter_block):
                # Пропускаем экранированный символ
                i += 2
                continue
            elif chapter_block[i] == '`':
                # Нашли закрывающую обратную кавычку
                content_end = i
                found_end = True
                break
            i += 1
        
        if found_end and content_end > content_start:
            content = chapter_block[content_start:content_end]
            sections.append({
                'id': section_id,
                'title': section_title,
                'content': content
            })
    
    if sections:
        chapters_data.append({
            'id': chapter_id,
            'title': chapter_title,
            'sections': sections
        })
        print(f"  Глава '{chapter_id}': {len(sections)} секций")

total_sections = sum(len(ch['sections']) for ch in chapters_data)
print(f"\nВсего найдено секций: {total_sections}")

if total_sections == 0:
    print("ОШИБКА: Не удалось извлечь секции!")
    print("Возможно, формат файла отличается от ожидаемого")
    print("Убедитесь, что секции имеют формат: id: '...', title: '...', content: `...`")
    exit(1)

# Создаем markdown файлы и новый chapters.ts
new_chapters_ts = """import { Chapter } from '../types';

export const chapters: Chapter[] = [
"""

for chapter in chapters_data:
    # Экранируем кавычки в title для TypeScript
    safe_chapter_title = chapter['title'].replace("'", "\\'").replace('\n', ' ')
    
    new_chapters_ts += f"  {{\n    id: '{chapter['id']}',\n    title: '{safe_chapter_title}',\n    sections: [\n"
    
    for section in chapter['sections']:
        section_id = section['id']
        section_title = section['title']
        section_content = section['content']
        
        # Сохраняем markdown файл в оба места: src (для разработки) и public (для fetch)
        md_filename = f"{section_id}.md"
        md_path_src = f"src/content/chapters/{md_filename}"
        md_path_public = f"public/content/chapters/{md_filename}"
        
        # Создаем директорию public если её нет
        os.makedirs('public/content/chapters', exist_ok=True)
        
        # Очищаем content от экранированных символов
        clean_content = section_content
        # Заменяем \\n на реальные переносы строк
        clean_content = clean_content.replace('\\n', '\n')
        # Заменяем двойные обратные слеши на одинарные для LaTeX
        clean_content = clean_content.replace('\\\\tag', '\\tag')
        clean_content = clean_content.replace('\\\\rightarrow', '\\rightarrow')
        clean_content = clean_content.replace('\\\\ldots', '\\ldots')
        clean_content = clean_content.replace('\\`', '`')
        # Убираем лишние экранирования (но оставляем нужные для LaTeX)
        # Не заменяем все \\, так как в LaTeX нужны двойные слеши
        
        # Сохраняем в src (для резерва)
        with open(md_path_src, 'w', encoding='utf-8') as md_file:
            md_file.write(clean_content)
        
        # Сохраняем в public (для загрузки через fetch)
        with open(md_path_public, 'w', encoding='utf-8') as md_file:
            md_file.write(clean_content)
        
        print(f"  Создан: {md_path_src} и {md_path_public} ({len(clean_content)} символов)")
        
        # Экранируем кавычки в title для TypeScript
        safe_title = section_title.replace("'", "\\'").replace('\n', ' ')
        
        # Добавляем секцию в новый chapters.ts
        new_chapters_ts += f"      {{\n        id: '{section_id}',\n        title: '{safe_title}',\n        markdownFile: 'chapters/{md_filename}',\n      }},\n"
    
    new_chapters_ts += "    ],\n  },\n"

new_chapters_ts += "];\n"

# Сохраняем новый chapters.ts
backup_path = 'src/data/chapters.ts.backup'
if os.path.exists('src/data/chapters.ts') and file_size > 1000:
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f"\nСоздана резервная копия: {backup_path}")

with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
    f.write(new_chapters_ts)

print(f"\n✓ Создан новый chapters.ts с метаданными")
print(f"✓ Всего обработано секций: {total_sections}")
print(f"\nТеперь можно запустить проект: npm run dev")
