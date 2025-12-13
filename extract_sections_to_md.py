#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для извлечения content из chapters.ts в отдельные .md файлы
и создания нового chapters.ts с только метаданными
"""

import re
import os

# Создаем директорию для markdown файлов
os.makedirs('src/content/chapters', exist_ok=True)

# Читаем chapters.ts
with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим все секции
section_pattern = r"\{\s*id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*content:\s*`([^`]+)`"
sections = re.findall(section_pattern, content, re.DOTALL)

print(f"Найдено секций: {len(sections)}")

# Создаем новый chapters.ts с метаданными
new_chapters_ts = """import { Chapter } from '../types';

export const chapters: Chapter[] = [
"""

# Обрабатываем каждую секцию
current_chapter = None
current_sections = []

# Находим все главы и их секции
chapter_pattern = r"\{\s*id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*sections:\s*\[(.*?)\]\s*\}"
chapters_data = re.findall(chapter_pattern, content, re.DOTALL)

for chapter_match in chapters_data:
    chapter_id = chapter_match[0]
    chapter_title = chapter_match[1]
    sections_content = chapter_match[2]
    
    # Находим все секции в этой главе
    section_matches = re.findall(
        r"\{\s*id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*content:\s*`([^`]+)`",
        sections_content,
        re.DOTALL
    )
    
    new_chapters_ts += f"  {{\n    id: '{chapter_id}',\n    title: '{chapter_title}',\n    sections: [\n"
    
    for section_id, section_title, section_content in section_matches:
        # Сохраняем markdown файл
        md_filename = f"{section_id}.md"
        md_path = f"src/content/chapters/{md_filename}"
        
        # Очищаем content от экранированных символов
        # Заменяем \\n на реальные переносы строк
        clean_content = section_content.replace('\\n', '\n')
        # Заменяем \\tag на \tag
        clean_content = clean_content.replace('\\\\tag', '\\tag')
        # Заменяем \\rightarrow на \rightarrow
        clean_content = clean_content.replace('\\\\rightarrow', '\\rightarrow')
        # Заменяем \\ldots на \ldots
        clean_content = clean_content.replace('\\\\ldots', '\\ldots')
        
        with open(md_path, 'w', encoding='utf-8') as md_file:
            md_file.write(clean_content)
        
        print(f"Создан файл: {md_path}")
        
        # Добавляем секцию в новый chapters.ts
        new_chapters_ts += f"      {{\n        id: '{section_id}',\n        title: '{section_title}',\n        markdownFile: 'chapters/{md_filename}',\n      }},\n"
    
    new_chapters_ts += "    ],\n  },\n"

new_chapters_ts += "];\n"

# Сохраняем новый chapters.ts
with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
    f.write(new_chapters_ts)

print(f"\nСоздан новый chapters.ts с метаданными")
print(f"Всего обработано секций: {len(sections)}")


