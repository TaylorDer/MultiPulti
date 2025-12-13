#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенное форматирование и обновление chapters.ts с полным текстом и изображениями
"""

import re
import json

def read_full_text():
    """Читает полный текст"""
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        return f.read()

def read_images_info():
    """Читает информацию об изображениях"""
    try:
        with open('extracted_images.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def format_text_for_markdown(text):
    """Форматирует текст для Markdown с правильными заголовками и формулами"""
    # Удаляем маркеры страниц
    text = re.sub(r'=== Страница \d+ ===\n', '', text)
    
    # Заменяем заголовки
    text = re.sub(r'^ВВЕДЕНИЕ$', '# Введение', text, flags=re.MULTILINE)
    text = re.sub(r'^Лабораторная работа (\d+)\.(\d+)$', r'# Лабораторная работа \1.\2', text, flags=re.MULTILINE)
    text = re.sub(r'^Практическая работа (\d+)\.(\d+)$', r'# Практическая работа \1.\2', text, flags=re.MULTILINE)
    text = re.sub(r'^КУРСОВАЯ РАБОТА$', '# Курсовая работа', text, flags=re.MULTILINE)
    
    # Заменяем подзаголовки
    text = re.sub(r'^([А-Я][А-Я\s]{15,})$', r'## \1', text, flags=re.MULTILINE)
    text = re.sub(r'^Цель:', '**Цель:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Задание:', '**Задание:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Общие положения$', '## Общие положения', text, flags=re.MULTILINE)
    text = re.sub(r'^ОБЩИЕ ПОЛОЖЕНИЯ$', '## Общие положения', text, flags=re.MULTILINE)
    text = re.sub(r'^Порядок выполнения работы$', '## Порядок выполнения работы', text, flags=re.MULTILINE)
    text = re.sub(r'^Содержание отчета$', '## Содержание отчета', text, flags=re.MULTILINE)
    text = re.sub(r'^Контрольные вопросы$', '## Контрольные вопросы', text, flags=re.MULTILINE)
    text = re.sub(r'^КОНТРОЛЬНЫЕ ВОПРОСЫ$', '## Контрольные вопросы', text, flags=re.MULTILINE)
    
    # Форматируем уравнения - оборачиваем в $$
    # Уравнения вида "dC/dτ = ..." или "dM(τ)/dτ = ..."
    text = re.sub(r'(\bd\w+\([^)]*\)/d\w+\s*=\s*[^\n]+)', r'$$\\1$$', text)
    text = re.sub(r'(\bd\w+/d\w+\s*=\s*[^\n]+)', r'$$\\1$$', text)
    
    # Уравнения вида "∂C/∂τ = ..."
    text = re.sub(r'(\b∂\w+/∂\w+\s*=\s*[^\n]+)', r'$$\\1$$', text)
    
    # Форматируем номера уравнений (1.42), (1.43) и т.д.
    text = re.sub(r'\((\d+)\.(\d+)\);', r'\\tag{\1.\2}', text)
    text = re.sub(r'\((\d+)\.(\d+)\)', r'\\tag{\1.\2}', text)
    
    # Заменяем специальные символы для LaTeX
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    text = text.replace('×', '\\times')
    text = text.replace('·', '\\cdot')
    
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Форматируем списки
    text = re.sub(r'^(\d+)\.\s+', r'\1. ', text, flags=re.MULTILINE)
    
    return text.strip()

def add_image_references(text, images_info):
    """Добавляет ссылки на изображения в текст"""
    # Создаем маппинг страниц к изображениям
    page_to_images = {}
    for img in images_info:
        page = img['page']
        if page not in page_to_images:
            page_to_images[page] = []
        page_to_images[page].append(img)
    
    # Ищем упоминания рисунков в тексте
    # Паттерны: "рис. 1.2", "Рис. 1.2", "рисунок 1.2"
    pattern = r'(рис\.?\s*(\d+)\.(\d+)|Рис\.?\s*(\d+)\.(\d+)|рисунок\s*(\d+)\.(\d+))'
    
    def replace_figure(match):
        fig_text = match.group(0)
        # Извлекаем номер рисунка
        chapter = match.group(2) or match.group(4) or match.group(6)
        figure = match.group(3) or match.group(5) or match.group(7)
        
        # Пытаемся найти соответствующее изображение
        # (это приблизительно, так как нужно знать точное соответствие)
        # Пока просто добавляем placeholder
        return f'{fig_text}\n\n![Рисунок {chapter}.{figure}](/images/placeholder.png)'
    
    # Пока не заменяем автоматически, так как нужно точное соответствие
    # text = re.sub(pattern, replace_figure, text, flags=re.IGNORECASE)
    
    return text

def find_section_in_text(text, start_keywords, end_keywords):
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
            if keyword in lines[i] and i > start_idx + 10:
                end_idx = i
                break
        if end_idx < len(lines):
            break
    
    return '\n'.join(lines[start_idx:end_idx]).strip()

def escape_for_typescript(text):
    """Экранирует для TypeScript template string"""
    text = text.replace('\\', '\\\\')
    text = text.replace('`', '\\`')
    text = text.replace('${', '\\${')
    text = text.replace('\r\n', '\\n')
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\n')
    return text

def update_all_sections():
    """Обновляет все секции в chapters.ts"""
    print("Чтение полного текста...")
    full_text = read_full_text()
    
    print("Чтение информации об изображениях...")
    images_info = read_images_info()
    print(f"Найдено изображений: {len(images_info)}")
    
    print("Чтение chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Определяем все секции
    sections = [
        {
            'id': 'introduction-1',
            'start': ['ВВЕДЕНИЕ'],
            'end': ['1. ПОСТРОЕНИЕ МАТЕМАТИЧЕСКИХ МОДЕЛЕЙ', '1. ПОСТРОЕНИЕ']
        },
        {
            'id': 'chapter1-lab1',
            'start': ['Лабораторная работа 1.1'],
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
    
    updated = 0
    for section in sections:
        print(f"\nОбработка: {section['id']}...")
        content = find_section_in_text(full_text, section['start'], section['end'])
        
        if content and len(content) > 100:
            # Форматируем
            formatted = format_text_for_markdown(content)
            # Добавляем ссылки на изображения
            formatted = add_image_references(formatted, images_info)
            # Экранируем
            escaped = escape_for_typescript(formatted)
            
            # Ищем и заменяем
            pattern = rf"(id: '{section['id']}'[^`]*?content: `)([^`]*?)(`[,\)])"
            
            def replacer(m):
                return m.group(1) + escaped + m.group(3)
            
            new_ts = re.sub(pattern, replacer, chapters_ts, flags=re.DOTALL)
            if new_ts != chapters_ts:
                chapters_ts = new_ts
                updated += 1
                print(f"  ✓ Обновлено ({len(escaped)} символов)")
            else:
                print(f"  ✗ Паттерн не найден")
        else:
            print(f"  ✗ Контент не найден или слишком короткий")
    
    if updated > 0:
        print(f"\nСохранение... ({updated} секций обновлено)")
        with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
            f.write(chapters_ts)
        print("Готово!")
    else:
        print("\nНичего не обновлено.")

if __name__ == "__main__":
    update_all_sections()

