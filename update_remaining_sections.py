#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обновление оставшихся секций (2.1, 2.3, 2.4, 2.6)
"""

import re

def read_text():
    with open('extracted_text.txt', 'r', encoding='utf-8') as f:
        return f.read()

def find_section(text, start_keywords, end_keywords):
    """Находит секцию в тексте"""
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
        return None
    
    end_idx = len(lines)
    for i in range(start_idx + 10, len(lines)):
        for keyword in end_keywords:
            if keyword in lines[i]:
                end_idx = i
                break
        if end_idx < len(lines):
            break
    
    return '\n'.join(lines[start_idx:end_idx]).strip()

def escape_ts(text):
    text = text.replace('\\', '\\\\')
    text = text.replace('`', '\\`')
    text = text.replace('${', '\\${')
    text = text.replace('\r\n', '\\n')
    text = text.replace('\n', '\\n')
    return text

def format_md(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    return text.strip()

def main():
    full_text = read_text()
    
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Секции для обновления
    sections_to_update = [
        {
            'id': 'chapter2-lab1',
            'start': ['Лабораторная работа 2.1'],
            'end': ['Лабораторная работа 2.2']
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
            'id': 'chapter2-lab6',
            'start': ['Лабораторная работа 2.6'],
            'end': ['3. ВАРИАЦИОННЫЕ', 'Практическая работа 3.1']
        },
    ]
    
    for section in sections_to_update:
        print(f"Обработка: {section['id']}...")
        content = find_section(full_text, section['start'], section['end'])
        
        if content and len(content) > 100:
            formatted = format_md(content)
            escaped = escape_ts(formatted)
            
            # Ищем по id и заменяем весь content блок
            # Более гибкий паттерн - ищем от id до следующего id или конца массива
            pattern = rf"(id: '{section['id']}'[^`]*?content: `)[^`]*?(`[,\)])"
            
            def repl(m):
                return m.group(1) + escaped + m.group(2)
            
            new_ts = re.sub(pattern, repl, chapters_ts, flags=re.DOTALL)
            if new_ts != chapters_ts:
                chapters_ts = new_ts
                print(f"  ✓ Обновлено ({len(escaped)} символов)")
            else:
                print(f"  ✗ Паттерн не найден")
        else:
            print(f"  ✗ Контент не найден")
    
    print("\nСохранение...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(chapters_ts)
    print("Готово!")

if __name__ == "__main__":
    main()

