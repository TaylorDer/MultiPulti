#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для извлечения content из chapters.ts в отдельные .md файлы
Парсит TypeScript файл построчно, учитывая многострочные строки
"""

import re
import os

# Создаем директорию для markdown файлов
os.makedirs('src/content/chapters', exist_ok=True)

# Читаем chapters.ts
with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Парсим файл построчно
chapters = []
current_chapter = None
current_section = None
in_content = False
content_lines = []
content_start_line = None

i = 0
while i < len(lines):
    line = lines[i]
    
    # Ищем начало главы
    if re.match(r'\s*\{\s*$', line) and current_chapter is None:
        # Проверяем следующую строку на id
        if i + 1 < len(lines) and 'id:' in lines[i + 1]:
            current_chapter = {'sections': []}
            i += 1
            continue
    
    # Ищем id главы
    if current_chapter and 'id:' in line and 'chapter' in line.lower() and current_chapter.get('id') is None:
        match = re.search(r"id:\s*['\"]([^'\"]+)['\"]", line)
        if match:
            current_chapter['id'] = match.group(1)
    
    # Ищем title главы
    if current_chapter and 'title:' in line and current_chapter.get('title') is None:
        match = re.search(r"title:\s*['\"]([^'\"]+)['\"]", line)
        if match:
            current_chapter['title'] = match.group(1)
    
    # Ищем начало секции
    if 'sections:' in line and '[' in line:
        # Начинаем собирать секции
        pass
    
    # Ищем начало секции внутри sections
    if re.match(r'\s*\{\s*$', line) and current_chapter and current_section is None:
        # Проверяем следующую строку на id секции
        if i + 1 < len(lines) and 'id:' in lines[i + 1]:
            current_section = {}
            i += 1
            continue
    
    # Ищем id секции
    if current_section and 'id:' in line and current_section.get('id') is None:
        match = re.search(r"id:\s*['\"]([^'\"]+)['\"]", line)
        if match:
            current_section['id'] = match.group(1)
    
    # Ищем title секции
    if current_section and 'title:' in line and current_section.get('title') is None:
        match = re.search(r"title:\s*['\"]([^'\"]+)['\"]", line)
        if match:
            current_section['title'] = match.group(1)
    
    # Ищем начало content
    if current_section and 'content:' in line and '`' in line:
        in_content = True
        content_lines = []
        # Извлекаем начало content из той же строки
        match = re.search(r"content:\s*`(.*)", line)
        if match:
            content_lines.append(match.group(1))
        i += 1
        continue
    
    # Собираем content
    if in_content:
        if '`' in line:
            # Конец content
            match = re.search(r"^(.*)`", line)
            if match:
                content_lines.append(match.group(1))
            # Сохраняем секцию
            content = '\n'.join(content_lines)
            current_section['content'] = content
            current_chapter['sections'].append(current_section)
            current_section = None
            in_content = False
            content_lines = []
        else:
            content_lines.append(line.rstrip('\n'))
        i += 1
        continue
    
    # Ищем конец главы
    if current_chapter and re.match(r'\s*\},\s*$', line) and not in_content:
        if current_chapter.get('id'):
            chapters.append(current_chapter)
        current_chapter = None
        current_section = None
    
    i += 1

print(f"Найдено глав: {len(chapters)}")
total_sections = sum(len(ch['sections']) for ch in chapters)
print(f"Найдено секций: {total_sections}")

# Создаем markdown файлы и новый chapters.ts
new_chapters_ts = """import { Chapter } from '../types';

export const chapters: Chapter[] = [
"""

for chapter in chapters:
    new_chapters_ts += f"  {{\n    id: '{chapter['id']}',\n    title: '{chapter['title']}',\n    sections: [\n"
    
    for section in chapter['sections']:
        section_id = section['id']
        section_title = section['title']
        section_content = section.get('content', '')
        
        # Сохраняем markdown файл
        md_filename = f"{section_id}.md"
        md_path = f"src/content/chapters/{md_filename}"
        
        # Очищаем content
        clean_content = section_content.replace('\\n', '\n')
        clean_content = clean_content.replace('\\\\tag', '\\tag')
        clean_content = clean_content.replace('\\\\rightarrow', '\\rightarrow')
        clean_content = clean_content.replace('\\\\ldots', '\\ldots')
        clean_content = clean_content.replace('\\`', '`')
        
        with open(md_path, 'w', encoding='utf-8') as md_file:
            md_file.write(clean_content)
        
        print(f"Создан файл: {md_path} ({len(clean_content)} символов)")
        
        # Добавляем секцию в новый chapters.ts
        new_chapters_ts += f"      {{\n        id: '{section_id}',\n        title: '{section_title}',\n        markdownFile: 'chapters/{md_filename}',\n      }},\n"
    
    new_chapters_ts += "    ],\n  },\n"

new_chapters_ts += "];\n"

# Сохраняем новый chapters.ts
with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
    f.write(new_chapters_ts)

print(f"\nСоздан новый chapters.ts с метаданными")


