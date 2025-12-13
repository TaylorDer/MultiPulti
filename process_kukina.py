#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обработки файла kukina_extracted.txt и добавления контента в chapters.ts
"""

import re

def fix_formulas(text):
    """Исправляет формулы, которые могли испортиться при извлечении из docx"""
    # Заменяем \tag{...} на правильный формат LaTeX
    text = re.sub(r'\\tag\{([^}]+)\}', r'\\tag{\1}', text)
    
    # Исправляем разорванные формулы
    # Если видим что-то вроде "dMτ(τ) = m" - это должно быть "dM(τ)/dτ = m"
    text = re.sub(r'd([A-Z])τ\(τ\)\s*=\s*', r'd\1(τ)/dτ = ', text)
    text = re.sub(r'd\s*\(([^)]+)\)\s*τ\s*=', r'd(\1)/dτ =', text)
    text = re.sub(r'd\s*\(([^)]+)\)\s*τ\s*\)', r'd(\1)/dτ)', text)
    
    # Исправляем частные производные
    text = re.sub(r'∂([A-Z])∂τ\s*=', r'∂\1/∂τ =', text)
    text = re.sub(r'∂([A-Z])∂l\s*=', r'∂\1/∂l =', text)
    
    return text

def read_kukina_file():
    """Читает файл kukina_extracted.txt"""
    with open('kukina_extracted.txt', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    content = read_kukina_file()
    print(f"Файл прочитан, длина: {len(content)} символов")
    print(f"Количество строк: {len(content.splitlines())}")
    
    # Найдем все лабораторные работы
    labs = re.findall(r'Лабораторная работа \d+\.\d+', content)
    print(f"\nНайдено лабораторных работ: {len(labs)}")
    for lab in labs[:10]:  # Показываем первые 10
        print(f"  - {lab}")


