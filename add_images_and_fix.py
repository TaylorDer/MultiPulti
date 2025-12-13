#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавление ссылок на изображения и исправление chapter3-lab1
"""

import re
import json

def read_full_text():
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        return f.read()

def read_images():
    try:
        with open('extracted_images.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def add_image_links(text, images_info):
    """Добавляет ссылки на изображения в текст"""
    # Маппинг рисунков к изображениям (приблизительный, на основе номеров страниц)
    # рис. 1.1 - page_2 или page_3
    # рис. 1.2 - page_39 (примерно)
    # и т.д.
    
    figure_mapping = {
        'рис. 1.1': '/images/page_2_img_1.png',
        'Рис. 1.1': '/images/page_2_img_1.png',
        'рис. 1.2': '/images/page_39_img_1.png',
        'Рис. 1.2': '/images/page_39_img_1.png',
        'рис. 1.3': '/images/page_39_img_1.png',
        'Рис. 1.3': '/images/page_39_img_1.png',
        'рис. 1.4': '/images/page_48_img_1.png',
        'Рис. 1.4': '/images/page_48_img_1.png',
        'рис. 1.5': '/images/page_49_img_1.png',
        'Рис. 1.5': '/images/page_49_img_1.png',
        'рис. 1.6': '/images/page_51_img_1.png',
        'Рис. 1.6': '/images/page_51_img_1.png',
        'рис. 1.7': '/images/page_57_img_1.png',
        'Рис. 1.7': '/images/page_57_img_1.png',
        'рис. 1.8': '/images/page_57_img_1.png',
        'Рис. 1.8': '/images/page_57_img_1.png',
        'рис. 2.1': '/images/page_2_img_2.png',
        'Рис. 2.1': '/images/page_2_img_2.png',
    }
    
    # Заменяем упоминания рисунков на ссылки
    for fig_text, img_path in figure_mapping.items():
        # Ищем паттерн "рис. X.Y" или "Рис. X.Y" и добавляем изображение после него
        pattern = rf'({re.escape(fig_text)}\.[^\n]*)'
        replacement = rf'\1\n\n![{fig_text}]({img_path})'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def format_text(text):
    """Форматирует текст"""
    # Удаляем маркеры страниц
    text = re.sub(r'=== Страница \d+ ===\n', '', text)
    
    # Заголовки
    text = re.sub(r'^ВВЕДЕНИЕ$', '# Введение', text, flags=re.MULTILINE)
    text = re.sub(r'^Лабораторная работа (\d+)\.(\d+)$', r'# Лабораторная работа \1.\2', text, flags=re.MULTILINE)
    text = re.sub(r'^Практическая работа (\d+)\.(\d+)$', r'# Практическая работа \1.\2', text, flags=re.MULTILINE)
    text = re.sub(r'^КУРСОВАЯ РАБОТА$', '# Курсовая работа', text, flags=re.MULTILINE)
    
    # Подзаголовки
    text = re.sub(r'^Цель:', '**Цель:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Задание:', '**Задание:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Общие положения$', '## Общие положения', text, flags=re.MULTILINE)
    text = re.sub(r'^ОБЩИЕ ПОЛОЖЕНИЯ$', '## Общие положения', text, flags=re.MULTILINE)
    text = re.sub(r'^Порядок выполнения работы$', '## Порядок выполнения работы', text, flags=re.MULTILINE)
    text = re.sub(r'^Содержание отчета$', '## Содержание отчета', text, flags=re.MULTILINE)
    text = re.sub(r'^Контрольные вопросы$', '## Контрольные вопросы', text, flags=re.MULTILINE)
    text = re.sub(r'^КОНТРОЛЬНЫЕ ВОПРОСЫ$', '## Контрольные вопросы', text, flags=re.MULTILINE)
    
    # Специальные символы
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    text = text.replace('×', '\\times')
    
    # Очистка
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

def find_section(text, start_kw, end_kw):
    lines = text.split('\n')
    start_idx = None
    
    for i, line in enumerate(lines):
        for kw in start_kw:
            if kw in line:
                start_idx = i
                break
        if start_idx is not None:
            break
    
    if start_idx is None:
        return None
    
    end_idx = len(lines)
    for i in range(start_idx + 10, len(lines)):
        for kw in end_kw:
            if kw in lines[i] and i > start_idx + 10:
                end_idx = i
                break
        if end_idx < len(lines):
            break
    
    return '\n'.join(lines[start_idx:end_idx]).strip()

def main():
    full_text = read_full_text()
    images = read_images()
    
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Исправляем chapter3-lab1
    print("Исправление chapter3-lab1...")
    lab3_1_content = find_section(full_text, ['Лабораторная работа 3.1'], ['Лабораторная работа 3.2'])
    
    if lab3_1_content and len(lab3_1_content) > 100:
        formatted = format_text(lab3_1_content)
        formatted = add_image_links(formatted, images)
        escaped = escape_ts(formatted)
        
        pattern = rf"(id: 'chapter3-lab1'[^`]*?content: `)([^`]*?)(`[,\)])"
        new_ts = re.sub(pattern, lambda m: m.group(1) + escaped + m.group(3), chapters_ts, flags=re.DOTALL)
        if new_ts != chapters_ts:
            chapters_ts = new_ts
            print(f"  ✓ Обновлено ({len(escaped)} символов)")
        else:
            print("  ✗ Паттерн не найден")
    else:
        print("  ✗ Контент не найден")
    
    # Добавляем изображения во все секции
    print("\nДобавление ссылок на изображения...")
    # Находим все content блоки и добавляем изображения
    pattern = r"(content: `)(.*?)(`[,\)])"
    
    def add_images_to_content(match):
        content = match.group(2)
        # Распаковываем
        content = content.replace('\\n', '\n')
        # Добавляем ссылки
        content = add_image_links(content, images)
        # Упаковываем обратно
        content = content.replace('\n', '\\n')
        content = content.replace('`', '\\`')
        content = content.replace('${', '\\${')
        return match.group(1) + content + match.group(3)
    
    chapters_ts = re.sub(pattern, add_images_to_content, chapters_ts, flags=re.DOTALL)
    
    print("Сохранение...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(chapters_ts)
    print("Готово!")

if __name__ == "__main__":
    main()

