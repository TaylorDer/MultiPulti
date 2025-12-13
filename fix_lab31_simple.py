#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простое исправление chapter3-lab1
"""

import re

def read_full_text():
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        return f.read()

def format_text(text):
    text = re.sub(r'=== Страница \d+ ===\n', '', text)
    text = re.sub(r'^Лабораторная работа 3\.2$', '# Лабораторная работа 3.1', text, flags=re.MULTILINE)
    text = re.sub(r'^Цель:', '**Цель:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Задание:', '**Задание:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Общие положения$', '## Общие положения', text, flags=re.MULTILINE)
    text = re.sub(r'^Порядок выполнения работы$', '## Порядок выполнения работы', text, flags=re.MULTILINE)
    text = re.sub(r'^Содержание отчета$', '## Содержание отчета', text, flags=re.MULTILINE)
    text = re.sub(r'^Контрольные вопросы$', '## Контрольные вопросы', text, flags=re.MULTILINE)
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def escape_ts(text):
    text = text.replace('\\', '\\\\')
    text = text.replace('`', '\\`')
    text = text.replace('${', '\\${')
    text = text.replace('\r\n', '\\n')
    text = text.replace('\n', '\\n')
    return text

def main():
    full_text = read_full_text()
    lines = full_text.split('\n')
    
    # Ищем строку с "Лабораторная работа 3.2" и "ЧИСЛЕННОЕ РЕШЕНИЕ"
    start_idx = None
    for i in range(len(lines)):
        if 'Лабораторная работа 3.2' in lines[i]:
            # Проверяем следующие строки
            for j in range(i, min(i+5, len(lines))):
                if 'ЧИСЛЕННОЕ РЕШЕНИЕ УРАВНЕНИЯ ЭЙЛЕРА' in lines[j]:
                    start_idx = i
                    break
        if start_idx is not None:
            break
    
    if start_idx is None:
        print("Не найдено начало работы 3.1")
        return
    
    # Ищем конец
    end_idx = len(lines)
    for i in range(start_idx + 10, len(lines)):
        if 'Лабораторная работа 3.2' in lines[i] and 'ПРЯМЫМИ МЕТОДАМИ' in (lines[i+1] if i+1 < len(lines) else ''):
            end_idx = i
            break
    
    content = '\n'.join(lines[start_idx:end_idx]).strip()
    content = re.sub(r'^Лабораторная работа 3\.2$', 'Лабораторная работа 3.1', content, flags=re.MULTILINE)
    
    print(f"Найден текст ({len(content)} символов)")
    
    formatted = format_text(content)
    escaped = escape_ts(formatted)
    
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    pattern = rf"(id: 'chapter3-lab1'[^`]*?content: `)([^`]*?)(`[,\)])"
    new_ts = re.sub(pattern, lambda m: m.group(1) + escaped + m.group(3), chapters_ts, flags=re.DOTALL)
    
    if new_ts != chapters_ts:
        with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
            f.write(new_ts)
        print(f"✓ Обновлено ({len(escaped)} символов)")
    else:
        print("✗ Паттерн не найден")

if __name__ == "__main__":
    main()

