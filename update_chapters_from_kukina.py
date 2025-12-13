#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления chapters.ts из файла kukina_extracted.txt
"""

import re
import json

def fix_formulas(text):
    """Исправляет формулы, которые могли испортиться при извлечении из docx"""
    # Исправляем разорванные производные
    text = re.sub(r'd([A-Z])τ\(τ\)\s*=\s*', r'd\1(τ)/dτ = ', text)
    text = re.sub(r'd\s*\(([^)]+)\)\s*τ\s*=', r'd(\1)/dτ =', text)
    text = re.sub(r'd\s*\(([^)]+)\)\s*τ\s*\)', r'd(\1)/dτ)', text)
    
    # Исправляем частные производные
    text = re.sub(r'∂([A-Z])∂τ\s*=', r'∂\1/∂τ =', text)
    text = re.sub(r'∂([A-Z])∂l\s*=', r'∂\1/∂l =', text)
    text = re.sub(r'∂∂([A-Z])τ\s*=', r'∂\1/∂τ =', text)
    text = re.sub(r'∂∂([A-Z])l\s*=', r'∂\1/∂l =', text)
    
    # Исправляем формулы с \tag
    text = re.sub(r'\\tag\{([^}]+)\}', r'(\\1)', text)
    
    # Исправляем разорванные формулы вида "f (x)" -> "f_0(x)"
    text = re.sub(r'f\s+0\s*\(', r'f_0(', text)
    text = re.sub(r'f\s+([0-9])\s*\(', r'f_\1(', text)
    
    return text

def convert_to_markdown(text):
    """Конвертирует текст в Markdown формат"""
    # Заменяем двойные переносы строк на одинарные
    text = re.sub(r'\n\n+', '\n\n', text)
    
    # Форматируем заголовки
    text = re.sub(r'^([А-Я][А-Я\s]+)$', r'## \1', text, flags=re.MULTILINE)
    
    # Форматируем формулы в LaTeX
    # Ищем формулы вида (1.1), (2.3) и т.д.
    text = re.sub(r'\((\d+\.\d+)\)', r'(\\1)', text)
    
    return text

def read_kukina_file():
    """Читает файл kukina_extracted.txt"""
    with open('kukina_extracted.txt', 'r', encoding='utf-8') as f:
        return f.read()

def extract_sections(content):
    """Извлекает разделы из контента"""
    sections = {}
    
    # Находим все лабораторные работы
    lab_pattern = r'Лабораторная работа (\d+)\.(\d+)\s*\n(.*?)(?=Лабораторная работа|\Z)'
    labs = re.finditer(lab_pattern, content, re.DOTALL)
    
    for lab in labs:
        chapter_num = lab.group(1)
        lab_num = lab.group(2)
        lab_content = lab.group(3).strip()
        
        key = f'chapter{chapter_num}-lab{lab_num}'
        sections[key] = {
            'title': f'Лабораторная работа {chapter_num}.{lab_num}',
            'content': fix_formulas(convert_to_markdown(lab_content))
        }
    
    return sections

if __name__ == '__main__':
    print("Чтение файла kukina_extracted.txt...")
    content = read_kukina_file()
    print(f"Файл прочитан, длина: {len(content)} символов")
    
    print("Извлечение разделов...")
    sections = extract_sections(content)
    print(f"Найдено разделов: {len(sections)}")
    
    for key, section in list(sections.items())[:5]:
        print(f"  - {key}: {section['title'][:50]}...")


