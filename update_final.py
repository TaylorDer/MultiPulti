#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальное обновление оставшихся секций
"""

import re

def read_text():
    with open('extracted_text.txt', 'r', encoding='utf-8') as f:
        return f.read()

def find_section_lines(text, start_keywords, end_keywords):
    """Находит секцию построчно"""
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

def escape_for_template(text):
    """Экранирует для TypeScript template string"""
    # Сначала защищаем обратные слеши в LaTeX командах
    # Заменяем обратные кавычки
    text = text.replace('`', '\\`')
    # Заменяем ${ 
    text = text.replace('${', '\\${')
    # Заменяем переносы
    text = text.replace('\r\n', '\\n')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\n')
    # Двойные обратные слеши для LaTeX
    text = text.replace('\\', '\\\\')
    return text

def format_text(text):
    """Форматирует текст"""
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.replace('≤', '\\\\leq')
    text = text.replace('≥', '\\\\geq')
    text = text.replace('→', '\\\\rightarrow')
    text = text.replace('°', '^\\\\circ')
    text = text.replace('×', '\\\\times')
    return text.strip()

def update_sections():
    full_text = read_text()
    
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    sections = [
        ('chapter2-lab1', ['Лабораторная работа 2.1'], ['Лабораторная работа 2.2']),
        ('chapter2-lab3', ['Лабораторная работа 2.3'], ['Лабораторная работа 2.4']),
        ('chapter2-lab4', ['Лабораторная работа 2.4'], ['Лабораторная работа 2.5']),
        ('chapter2-lab6', ['Лабораторная работа 2.6'], ['3. ВАРИАЦИОННЫЕ', 'Практическая работа 3.1']),
    ]
    
    for section_id, start_kw, end_kw in sections:
        print(f"Обработка: {section_id}...")
        content = find_section_lines(full_text, start_kw, end_kw)
        
        if content and len(content) > 100:
            formatted = format_text(content)
            escaped = escape_for_template(formatted)
            
            # Ищем блок от id до следующего id или конца массива sections
            # Используем более сложный паттерн
            pattern = rf"(id: '{section_id}'[^\n]*\n[^\n]*title:[^\n]*\n[^\n]*content: `)(.*?)(`\s*[,\)])"
            
            def replacer(m):
                return m.group(1) + escaped + m.group(3)
            
            new_ts = re.sub(pattern, replacer, chapters_ts, flags=re.DOTALL)
            if new_ts != chapters_ts:
                chapters_ts = new_ts
                print(f"  ✓ Обновлено ({len(escaped)} символов)")
            else:
                # Пробуем более простой паттерн
                pattern2 = rf"(id: '{section_id}'[^`]*content: `)([^`]*?)(`[,\)])"
                new_ts2 = re.sub(pattern2, lambda m: m.group(1) + escaped + m.group(3), chapters_ts, flags=re.DOTALL)
                if new_ts2 != chapters_ts:
                    chapters_ts = new_ts2
                    print(f"  ✓ Обновлено (вариант 2, {len(escaped)} символов)")
                else:
                    print(f"  ✗ Не удалось найти паттерн")
        else:
            print(f"  ✗ Контент не найден")
    
    print("\nСохранение...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(chapters_ts)
    print("Готово!")

if __name__ == "__main__":
    update_sections()

