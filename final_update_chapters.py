#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный скрипт для обновления chapters.ts полным текстом из PDF
"""

import json
import re

def escape_for_template_string(text):
    """Экранирует текст для использования в TypeScript template string"""
    # Заменяем обратные кавычки
    text = text.replace('`', '\\`')
    # Заменяем ${ на \${ чтобы не интерпретировалось как шаблонная строка
    text = text.replace('${', '\\${')
    # Заменяем обратные слеши (но сохраняем те, что нужны для LaTeX)
    # Сначала защищаем LaTeX команды
    text = re.sub(r'\\([a-zA-Z]+)', r'\\\\\\1', text)
    # Заменяем переносы строк
    text = text.replace('\n', '\\n')
    return text

def format_for_markdown(text):
    """Форматирует текст для Markdown"""
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Заменяем специальные символы для LaTeX
    replacements = {
        '≤': '\\leq',
        '≥': '\\geq',
        '→': '\\rightarrow',
        '°': '^\\circ',
        '×': '\\times',
        '·': '\\cdot',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Форматируем заголовки
    text = re.sub(r'^([А-Я][А-Я\s]+)$', r'## \1', text, flags=re.MULTILINE)
    
    return text.strip()

def read_chapters_ts():
    """Читает текущий chapters.ts"""
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        return f.read()

def update_chapters_with_full_text():
    """Обновляет chapters.ts полным текстом из JSON"""
    # Читаем извлеченные лабораторные работы
    with open('extracted_labs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Читаем текущий chapters.ts
    chapters_content = read_chapters_ts()
    
    # Маппинг ID секций к ключам в JSON
    section_mapping = {
        'introduction-1': 'introduction',
        'chapter1-lab1': '1.1',
        'chapter1-lab2': '1.2',
        'chapter1-lab3': '1.3',
        'chapter1-lab4': '1.4',
        'chapter1-lab5': '1.5',
        'chapter1-lab6': '1.6',
        'chapter1-lab7': '1.7',
        'chapter2-lab1': '2.1',
        'chapter2-lab2': '2.2',
        'chapter2-lab3': '2.3',
        'chapter2-lab4': '2.4',
        'chapter2-lab5': '2.5',
        'chapter2-lab6': '2.6',
        'chapter3-practice1': '3.practice',
        'chapter3-lab1': '3.1',
        'chapter3-lab2': '3.2',
        'chapter3-lab3': '3.3',
    }
    
    # Обновляем каждую секцию
    for section_id, json_key in section_mapping.items():
        if json_key in data.get('labs', {}):
            lab_text = data['labs'][json_key]
            # Форматируем текст
            formatted_text = format_for_markdown(lab_text)
            # Экранируем для template string
            escaped_text = escape_for_template_string(formatted_text)
            
            # Ищем паттерн content: `...` в chapters.ts
            pattern = rf"(id: '{section_id}'[^`]*content: `)([^`]*?)(`[,\)])"
            
            def replace_content(match):
                return match.group(1) + escaped_text + match.group(3)
            
            chapters_content = re.sub(pattern, replace_content, chapters_content, flags=re.DOTALL)
            print(f"Обновлена секция: {section_id}")
    
    # Обновляем введение
    if 'introduction' in data:
        intro_text = data['introduction']
        formatted_text = format_for_markdown(intro_text)
        escaped_text = escape_for_template_string(formatted_text)
        
        pattern = r"(id: 'introduction-1'[^`]*content: `)([^`]*?)(`[,\)])"
        chapters_content = re.sub(pattern, lambda m: m.group(1) + escaped_text + m.group(3), chapters_content, flags=re.DOTALL)
        print("Обновлено введение")
    
    # Сохраняем обновленный файл
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(chapters_content)
    
    print("\nФайл chapters.ts успешно обновлен!")

if __name__ == "__main__":
    update_chapters_with_full_text()

