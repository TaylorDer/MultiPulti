#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления форматирования markdown файлов
"""

import re
from pathlib import Path

def fix_markdown_file(filepath):
    """Исправляет форматирование в markdown файле"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Убираем двойное выделение в заголовках (# **текст** -> # текст)
    content = re.sub(r'^#\s+\*\*(.+?)\*\*$', r'# \1', content, flags=re.MULTILINE)
    
    # Убираем множественные ** в тексте
    content = re.sub(r'\*\*\*\*+', '**', content)
    
    # Исправляем двойные пробелы в начале строк
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        # Убираем множественные пробелы в начале (кроме отступов в коде)
        if not line.strip().startswith('```') and not line.strip().startswith('`'):
            line = re.sub(r'^ {2,}', '', line)
        fixed_lines.append(line)
    content = '\n'.join(fixed_lines)
    
    # Убираем множественные пустые строки (более 2 подряд)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    chapters_dirs = [
        Path('public/content/chapters'),
        Path('src/content/chapters')
    ]
    
    total_fixed = 0
    
    for chapters_dir in chapters_dirs:
        if not chapters_dir.exists():
            continue
        
        files = list(chapters_dir.glob('*.md'))
        print(f"\nОбрабатываю {len(files)} файлов в {chapters_dir}")
        
        for filepath in files:
            if fix_markdown_file(filepath):
                total_fixed += 1
                print(f"  ✓ {filepath.name}")
    
    print(f"\nВсего исправлено файлов: {total_fixed}")
    print("Готово!")

if __name__ == '__main__':
    main()

