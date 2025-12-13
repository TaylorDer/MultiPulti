#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления chapters.ts полным текстом из extracted_text.txt
"""

import re

def read_text():
    """Читает extracted_text.txt"""
    with open('extracted_text.txt', 'r', encoding='utf-8') as f:
        return f.read()

def extract_section(text, start_pattern, end_patterns):
    """Извлекает секцию между start_pattern и первым end_pattern"""
    match = re.search(start_pattern, text)
    if not match:
        return None
    
    start = match.start()
    
    # Ищем конец
    end = len(text)
    for pattern in end_patterns:
        search_start = start + 100  # Пропускаем начало, чтобы не найти тот же паттерн
        match = re.search(pattern, text[search_start:])
        if match:
            end = search_start + match.start()
            break
    
    return text[start:end].strip()

def escape_for_ts_template(text):
    """Экранирует текст для TypeScript template string"""
    # Заменяем обратные кавычки
    text = text.replace('`', '\\`')
    # Заменяем ${ на \${ 
    text = text.replace('${', '\\${')
    # Заменяем переносы строк на \n
    text = text.replace('\r\n', '\\n')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\n')
    return text

def format_markdown(text):
    """Форматирует текст для Markdown"""
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Заменяем специальные символы
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    text = text.replace('×', '\\times')
    return text.strip()

def update_chapters_ts():
    """Обновляет chapters.ts"""
    print("Чтение extracted_text.txt...")
    full_text = read_text()
    
    print("Чтение chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Маппинг секций
    sections = [
        {
            'id': 'introduction-1',
            'start': r'^ВВЕДЕНИЕ',
            'end': [r'^1\. ПОСТРОЕНИЕ МАТЕМАТИЧЕСКИХ МОДЕЛЕЙ']
        },
        {
            'id': 'chapter1-lab1',
            'start': r'^Лабораторная работа 1\.1',
            'end': [r'^Лабораторная работа 1\.2']
        },
        {
            'id': 'chapter1-lab2',
            'start': r'^Лабораторная работа 1\.2',
            'end': [r'^Лабораторная работа 1\.3']
        },
        {
            'id': 'chapter1-lab3',
            'start': r'^Лабораторная работа 1\.3',
            'end': [r'^Лабораторная работа 1\.4']
        },
        {
            'id': 'chapter1-lab4',
            'start': r'^Лабораторная работа 1\.4',
            'end': [r'^Лабораторная работа 1\.5']
        },
        {
            'id': 'chapter1-lab5',
            'start': r'^Лабораторная работа 1\.5',
            'end': [r'^Лабораторная работа 1\.6']
        },
        {
            'id': 'chapter1-lab6',
            'start': r'^Лабораторная работа 1\.6',
            'end': [r'^Лабораторная работа 1\.7']
        },
        {
            'id': 'chapter1-lab7',
            'start': r'^Лабораторная работа 1\.7',
            'end': [r'^2\. КОНЕЧНОМЕРНЫЕ ЗАДАЧИ']
        },
        {
            'id': 'chapter2-lab1',
            'start': r'^Лабораторная работа 2\.1',
            'end': [r'^Лабораторная работа 2\.2']
        },
        {
            'id': 'chapter2-lab2',
            'start': r'^Лабораторная работа 2\.2',
            'end': [r'^Лабораторная работа 2\.3']
        },
        {
            'id': 'chapter2-lab3',
            'start': r'^Лабораторная работа 2\.3',
            'end': [r'^Лабораторная работа 2\.4']
        },
        {
            'id': 'chapter2-lab4',
            'start': r'^Лабораторная работа 2\.4',
            'end': [r'^Лабораторная работа 2\.5']
        },
        {
            'id': 'chapter2-lab5',
            'start': r'^Лабораторная работа 2\.5',
            'end': [r'^Лабораторная работа 2\.6']
        },
        {
            'id': 'chapter2-lab6',
            'start': r'^Лабораторная работа 2\.6',
            'end': [r'^3\. ВАРИАЦИОННЫЕ ЗАДАЧИ', r'^Практическая работа 3\.1']
        },
        {
            'id': 'chapter3-practice1',
            'start': r'^Практическая работа 3\.1',
            'end': [r'^Лабораторная работа 3\.1', r'^Лабораторная работа 3\.2']
        },
        {
            'id': 'chapter3-lab1',
            'start': r'^Лабораторная работа 3\.1',
            'end': [r'^Лабораторная работа 3\.2']
        },
        {
            'id': 'chapter3-lab2',
            'start': r'^Лабораторная работа 3\.2',
            'end': [r'^Лабораторная работа 3\.3']
        },
        {
            'id': 'chapter3-lab3',
            'start': r'^Лабораторная работа 3\.3',
            'end': [r'^КУРСОВАЯ РАБОТА']
        },
        {
            'id': 'coursework-1',
            'start': r'^КУРСОВАЯ РАБОТА',
            'end': [r'^СПИСОК РЕКОМЕНДУЕМОЙ ЛИТЕРАТУРЫ']
        },
    ]
    
    # Обновляем каждую секцию
    for section in sections:
        print(f"Обработка секции: {section['id']}...")
        content = extract_section(full_text, section['start'], section['end'])
        
        if content:
            # Форматируем
            formatted = format_markdown(content)
            # Экранируем
            escaped = escape_for_ts_template(formatted)
            
            # Ищем и заменяем в chapters.ts
            # Паттерн для поиска content: `...` с нужным id
            pattern = rf"(id: '{section['id']}'[^`]*?content: `)([^`]*?)(`[,\)])"
            
            def replacer(m):
                return m.group(1) + escaped + m.group(3)
            
            new_chapters_ts = re.sub(pattern, replacer, chapters_ts, flags=re.DOTALL)
            if new_chapters_ts != chapters_ts:
                chapters_ts = new_chapters_ts
                print(f"  ✓ Обновлено ({len(escaped)} символов)")
            else:
                print(f"  ✗ Не найдено для замены")
        else:
            print(f"  ✗ Контент не найден")
    
    # Сохраняем
    print("\nСохранение обновленного chapters.ts...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(chapters_ts)
    
    print("Готово!")

if __name__ == "__main__":
    update_chapters_ts()

