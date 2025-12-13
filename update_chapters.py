#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления chapters.ts полным текстом из PDF
"""

import re
import json

def escape_for_typescript(text):
    """Экранирует текст для использования в TypeScript строке"""
    # Заменяем обратные слеши
    text = text.replace('\\', '\\\\')
    # Заменяем обратные кавычки
    text = text.replace('`', '\\`')
    # Заменяем ${ на \${ чтобы не интерпретировалось как шаблонная строка
    text = text.replace('${', '\\${')
    # Заменяем переносы строк на \n
    text = text.replace('\n', '\\n')
    return text

def clean_markdown_text(text):
    """Очищает и форматирует текст для Markdown"""
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы строк (оставляем максимум 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Заменяем специальные символы для LaTeX формул
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    text = text.replace('×', '\\times')
    text = text.replace('·', '\\cdot')
    # Исправляем формулы - добавляем $ где нужно
    # Паттерн для уравнений вида "dC/dτ = ..."
    text = re.sub(r'\bd(\w+)/d(\w+)\b', r'$\\frac{d\1}{d\2}$', text)
    # Паттерн для частных производных
    text = re.sub(r'\b∂(\w+)/∂(\w+)\b', r'$\\frac{\\partial \1}{\\partial \2}$', text)
    return text.strip()

def extract_lab_content(text, lab_num):
    """Извлекает содержание конкретной лабораторной работы"""
    # Ищем начало лабораторной работы
    pattern = rf'Лабораторная работа {lab_num[0]}\.{lab_num[1]}'
    match = re.search(pattern, text)
    if not match:
        return None
    
    start = match.start()
    
    # Ищем конец - следующую лабораторную работу или конец раздела
    next_patterns = [
        rf'Лабораторная работа {lab_num[0]}\.{lab_num[1] + 1}',
        rf'Лабораторная работа {lab_num[0] + 1}\.1',
        'КУРСОВАЯ РАБОТА',
        '2\. КОНЕЧНОМЕРНЫЕ',
        '3\. ВАРИАЦИОННЫЕ',
    ]
    
    end = len(text)
    for pattern in next_patterns:
        match = re.search(pattern, text[start + 100:])
        if match:
            end = start + 100 + match.start()
            break
    
    content = text[start:end].strip()
    return clean_markdown_text(content)

def read_extracted_text():
    """Читает извлеченный текст"""
    with open('extracted_text.txt', 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("Чтение extracted_text.txt...")
    full_text = read_extracted_text()
    
    # Извлекаем введение
    intro_match = re.search(r'ВВЕДЕНИЕ', full_text)
    chapter1_match = re.search(r'1\. ПОСТРОЕНИЕ МАТЕМАТИЧЕСКИХ МОДЕЛЕЙ', full_text)
    
    if intro_match and chapter1_match:
        introduction_text = full_text[intro_match.start():chapter1_match.start()].strip()
        print(f"Введение: {len(introduction_text)} символов")
    
    # Извлекаем лабораторные работы
    labs = {}
    
    # Раздел 1
    for i in range(1, 8):
        lab_content = extract_lab_content(full_text, (1, i))
        if lab_content:
            labs[f'1.{i}'] = lab_content
            print(f"Лабораторная работа 1.{i}: {len(lab_content)} символов")
    
    # Раздел 2
    for i in range(1, 7):
        lab_content = extract_lab_content(full_text, (2, i))
        if lab_content:
            labs[f'2.{i}'] = lab_content
            print(f"Лабораторная работа 2.{i}: {len(lab_content)} символов")
    
    # Раздел 3
    practice_content = extract_lab_content(full_text, (3, 1))
    if practice_content:
        labs['3.practice'] = practice_content
        print(f"Практическая работа 3.1: {len(practice_content)} символов")
    
    for i in range(1, 4):
        lab_content = extract_lab_content(full_text, (3, i))
        if lab_content:
            labs[f'3.{i}'] = lab_content
            print(f"Лабораторная работа 3.{i}: {len(lab_content)} символов")
    
    # Сохраняем результаты
    with open('extracted_labs.json', 'w', encoding='utf-8') as f:
        json.dump({
            'introduction': introduction_text if 'introduction_text' in locals() else '',
            'labs': labs
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\nИзвлечено {len(labs)} лабораторных работ")
    print("Результаты сохранены в extracted_labs.json")

if __name__ == "__main__":
    main()

