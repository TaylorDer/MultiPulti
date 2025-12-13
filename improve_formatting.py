#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшение форматирования текста в chapters.ts
"""

import re

def improve_markdown_formatting(text):
    """Улучшает форматирование текста для Markdown"""
    # Добавляем заголовки для лабораторных работ
    text = re.sub(r'^Лабораторная работа (\d+)\.(\d+)$', r'# Лабораторная работа \1.\2', text, flags=re.MULTILINE)
    text = re.sub(r'^Практическая работа (\d+)\.(\d+)$', r'# Практическая работа \1.\2', text, flags=re.MULTILINE)
    text = re.sub(r'^КУРСОВАЯ РАБОТА$', r'# Курсовая работа', text, flags=re.MULTILINE)
    text = re.sub(r'^ВВЕДЕНИЕ$', r'# Введение', text, flags=re.MULTILINE)
    
    # Добавляем заголовки для разделов
    text = re.sub(r'^([А-Я][А-Я\s]{10,})$', r'## \1', text, flags=re.MULTILINE)
    
    # Форматируем подзаголовки
    text = re.sub(r'^Цель:', r'**Цель:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Задание:', r'**Задание:**', text, flags=re.MULTILINE)
    text = re.sub(r'^Общие положения$', r'## Общие положения', text, flags=re.MULTILINE)
    text = re.sub(r'^Порядок выполнения работы$', r'## Порядок выполнения работы', text, flags=re.MULTILINE)
    text = re.sub(r'^Содержание отчета$', r'## Содержание отчета', text, flags=re.MULTILINE)
    text = re.sub(r'^Контрольные вопросы$', r'## Контрольные вопросы', text, flags=re.MULTILINE)
    
    # Форматируем уравнения - оборачиваем в $$
    # Паттерн для уравнений вида "dC/dτ = ..."
    text = re.sub(r'(\bd\w+/d\w+\s*=\s*[^\n]+)', r'$$\\1$$', text)
    # Паттерн для уравнений в скобках (1.42)
    text = re.sub(r'\((\d+)\.(\d+)\);', r'\\tag{\1.\2}', text)
    
    # Исправляем экранирование LaTeX
    text = text.replace('\\rightarrow', '\\\\rightarrow')
    text = text.replace('\\leq', '\\\\leq')
    text = text.replace('\\geq', '\\\\geq')
    text = text.replace('^\\circ', '^\\\\circ')
    
    return text

def main():
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все content блоки и улучшаем форматирование
    pattern = r"(content: `)(.*?)(`[,\)])"
    
    def improve_content(match):
        content_text = match.group(2)
        # Распаковываем \n обратно в переносы строк для обработки
        content_text = content_text.replace('\\n', '\n')
        # Улучшаем форматирование
        improved = improve_markdown_formatting(content_text)
        # Обратно упаковываем
        improved = improved.replace('\n', '\\n')
        improved = improved.replace('`', '\\`')
        improved = improved.replace('${', '\\${')
        return match.group(1) + improved + match.group(3)
    
    new_content = re.sub(pattern, improve_content, content, flags=re.DOTALL)
    
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Форматирование улучшено!")

if __name__ == "__main__":
    main()

