#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга лабораторных работ из extracted_text.txt
и подготовки контента для chapters.ts
"""

import re

def read_text_file(filename):
    """Читает текстовый файл"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def find_lab_sections(text):
    """Находит все лабораторные работы в тексте"""
    # Паттерны для поиска начала лабораторных работ
    patterns = [
        r'Лабораторная работа (\d+)\.(\d+)',
        r'Практическая работа (\d+)\.(\d+)',
        r'КУРСОВАЯ РАБОТА',
        r'ВВЕДЕНИЕ',
    ]
    
    sections = []
    lines = text.split('\n')
    
    current_section = None
    current_content = []
    
    for i, line in enumerate(lines):
        # Проверяем, является ли строка началом новой секции
        is_new_section = False
        section_type = None
        section_num = None
        
        if re.match(r'^ВВЕДЕНИЕ', line.strip()):
            is_new_section = True
            section_type = 'introduction'
        elif re.match(r'^Лабораторная работа (\d+)\.(\d+)', line.strip()):
            match = re.match(r'^Лабораторная работа (\d+)\.(\d+)', line.strip())
            section_type = 'lab'
            section_num = (int(match.group(1)), int(match.group(2)))
            is_new_section = True
        elif re.match(r'^Практическая работа (\d+)\.(\d+)', line.strip()):
            match = re.match(r'^Практическая работа (\d+)\.(\d+)', line.strip())
            section_type = 'practice'
            section_num = (int(match.group(1)), int(match.group(2)))
            is_new_section = True
        elif re.match(r'^КУРСОВАЯ РАБОТА', line.strip()):
            is_new_section = True
            section_type = 'coursework'
        
        if is_new_section:
            # Сохраняем предыдущую секцию
            if current_section:
                sections.append({
                    'type': current_section['type'],
                    'num': current_section.get('num'),
                    'content': '\n'.join(current_content).strip()
                })
            
            # Начинаем новую секцию
            current_section = {
                'type': section_type,
                'num': section_num
            }
            current_content = [line]
        else:
            if current_section:
                current_content.append(line)
    
    # Сохраняем последнюю секцию
    if current_section:
        sections.append({
            'type': current_section['type'],
            'num': current_section.get('num'),
            'content': '\n'.join(current_content).strip()
        })
    
    return sections

def clean_text(text):
    """Очищает текст от лишних пробелов и форматирует для Markdown"""
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Заменяем специальные символы для LaTeX
    text = text.replace('≤', '\\leq')
    text = text.replace('≥', '\\geq')
    text = text.replace('→', '\\rightarrow')
    text = text.replace('°', '^\\circ')
    return text.strip()

def main():
    print("Чтение extracted_text.txt...")
    text = read_text_file('extracted_text.txt')
    
    print("Поиск лабораторных работ...")
    sections = find_lab_sections(text)
    
    print(f"Найдено секций: {len(sections)}")
    
    # Сохраняем результаты
    with open('parsed_sections.txt', 'w', encoding='utf-8') as f:
        for i, section in enumerate(sections):
            f.write(f"\n{'='*80}\n")
            f.write(f"Секция {i+1}: {section['type']}")
            if section.get('num'):
                f.write(f" {section['num']}")
            f.write(f"\n{'='*80}\n")
            f.write(section['content'][:500])  # Первые 500 символов для проверки
            f.write("\n...\n")
    
    print("Результаты сохранены в parsed_sections.txt")
    print("\nПервые несколько секций:")
    for i, section in enumerate(sections[:5]):
        print(f"{i+1}. {section['type']} {section.get('num', '')} - {len(section['content'])} символов")

if __name__ == "__main__":
    main()

