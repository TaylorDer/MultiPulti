#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенный скрипт для обновления chapters.ts
"""

import re

def read_text():
    with open('extracted_text.txt', 'r', encoding='utf-8') as f:
        return f.read()

def find_section_boundaries(text, start_keywords, end_keywords):
    """Находит границы секции по ключевым словам"""
    lines = text.split('\n')
    
    start_idx = None
    for i, line in enumerate(lines):
        for keyword in start_keywords:
            if keyword in line:
                start_idx = i
                break
        if start_idx is not None:
            break
    
    if start_idx is None:
        return None, None
    
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        for keyword in end_keywords:
            if keyword in lines[i] and i > start_idx + 10:  # Минимум 10 строк после начала
                end_idx = i
                break
        if end_idx < len(lines):
            break
    
    content = '\n'.join(lines[start_idx:end_idx]).strip()
    return content, end_idx

def escape_for_ts(text):
    """Экранирует для TypeScript template string"""
    text = text.replace('\\', '\\\\')
    text = text.replace('`', '\\`')
    text = text.replace('${', '\\${')
    text = text.replace('\r\n', '\\n')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\n')
    return text

def format_text(text):
    """Форматирует текст"""
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Заменяем символы
    replacements = {
        '≤': '\\leq',
        '≥': '\\geq',
        '→': '\\rightarrow',
        '°': '^\\circ',
        '×': '\\times',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()

def update_chapters():
    full_text = read_text()
    
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Определяем секции
    sections = [
        {
            'id': 'introduction-1',
            'start': ['ВВЕДЕНИЕ'],
            'end': ['1. ПОСТРОЕНИЕ МАТЕМАТИЧЕСКИХ МОДЕЛЕЙ', '1. ПОСТРОЕНИЕ']
        },
        {
            'id': 'chapter1-lab1',
            'start': ['Лабораторная работа 1.1', 'Лабораторная работа 1.1'],
            'end': ['Лабораторная работа 1.2']
        },
        {
            'id': 'chapter1-lab2',
            'start': ['Лабораторная работа 1.2'],
            'end': ['Лабораторная работа 1.3']
        },
        {
            'id': 'chapter1-lab3',
            'start': ['Лабораторная работа 1.3'],
            'end': ['Лабораторная работа 1.4']
        },
        {
            'id': 'chapter1-lab4',
            'start': ['Лабораторная работа 1.4'],
            'end': ['Лабораторная работа 1.5']
        },
        {
            'id': 'chapter1-lab5',
            'start': ['Лабораторная работа 1.5'],
            'end': ['Лабораторная работа 1.6']
        },
        {
            'id': 'chapter1-lab6',
            'start': ['Лабораторная работа 1.6'],
            'end': ['Лабораторная работа 1.7']
        },
        {
            'id': 'chapter1-lab7',
            'start': ['Лабораторная работа 1.7'],
            'end': ['2. КОНЕЧНОМЕРНЫЕ', 'Лабораторная работа 2.1']
        },
        {
            'id': 'chapter2-lab1',
            'start': ['Лабораторная работа 2.1'],
            'end': ['Лабораторная работа 2.2']
        },
        {
            'id': 'chapter2-lab2',
            'start': ['Лабораторная работа 2.2'],
            'end': ['Лабораторная работа 2.3']
        },
        {
            'id': 'chapter2-lab3',
            'start': ['Лабораторная работа 2.3'],
            'end': ['Лабораторная работа 2.4']
        },
        {
            'id': 'chapter2-lab4',
            'start': ['Лабораторная работа 2.4'],
            'end': ['Лабораторная работа 2.5']
        },
        {
            'id': 'chapter2-lab5',
            'start': ['Лабораторная работа 2.5'],
            'end': ['Лабораторная работа 2.6']
        },
        {
            'id': 'chapter2-lab6',
            'start': ['Лабораторная работа 2.6'],
            'end': ['3. ВАРИАЦИОННЫЕ', 'Практическая работа 3.1']
        },
        {
            'id': 'chapter3-practice1',
            'start': ['Практическая работа 3.1'],
            'end': ['Лабораторная работа 3.1', 'Лабораторная работа 3.2']
        },
        {
            'id': 'chapter3-lab1',
            'start': ['Лабораторная работа 3.1'],
            'end': ['Лабораторная работа 3.2']
        },
        {
            'id': 'chapter3-lab2',
            'start': ['Лабораторная работа 3.2'],
            'end': ['Лабораторная работа 3.3']
        },
        {
            'id': 'chapter3-lab3',
            'start': ['Лабораторная работа 3.3'],
            'end': ['КУРСОВАЯ РАБОТА']
        },
        {
            'id': 'coursework-1',
            'start': ['КУРСОВАЯ РАБОТА'],
            'end': ['СПИСОК РЕКОМЕНДУЕМОЙ ЛИТЕРАТУРЫ']
        },
    ]
    
    updated_count = 0
    for section in sections:
        print(f"Обработка: {section['id']}...")
        content, _ = find_section_boundaries(full_text, section['start'], section['end'])
        
        if content and len(content) > 100:
            formatted = format_text(content)
            escaped = escape_for_ts(formatted)
            
            # Ищем паттерн в chapters.ts
            pattern = rf"(id: '{section['id']}'[^`]*?content: `)([^`]*?)(`[,\)])"
            
            def repl(m):
                return m.group(1) + escaped + m.group(3)
            
            new_ts = re.sub(pattern, repl, chapters_ts, flags=re.DOTALL)
            if new_ts != chapters_ts:
                chapters_ts = new_ts
                updated_count += 1
                print(f"  ✓ Обновлено ({len(escaped)} символов)")
            else:
                print(f"  ✗ Паттерн не найден в chapters.ts")
        else:
            print(f"  ✗ Контент не найден или слишком короткий")
    
    if updated_count > 0:
        print(f"\nСохранение... ({updated_count} секций обновлено)")
        with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
            f.write(chapters_ts)
        print("Готово!")
    else:
        print("\nНичего не обновлено. Проверьте паттерны.")

if __name__ == "__main__":
    update_chapters()

