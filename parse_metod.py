#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга metod.txt и разбиения на главы и секции
"""

import re
import os
from pathlib import Path

def read_file(filepath):
    """Читает файл с правильной кодировкой"""
    encodings = ['utf-8', 'cp1251', 'windows-1251']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Не удалось прочитать файл {filepath}")

def clean_text(text):
    """Очищает текст от лишних символов"""
    # Удаляем множественные пробелы
    text = re.sub(r' +', ' ', text)
    # Удаляем множественные переносы строк
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Убираем пробелы в начале и конце строк
    lines = [line.strip() for line in text.split('\n')]
    # Удаляем строки, которые являются только номерами страниц
    lines = [line for line in lines if not re.match(r'^[0-9]+$', line)]
    return '\n'.join(lines).strip()

def is_chapter_start(line):
    """Проверяет, является ли строка началом главы"""
    # Паттерн: "1. ОСНОВЫ..." или "2. ОСНОВЫ..."
    return re.match(r'^[0-9]+\.[\s]+[А-Я]', line.strip())

def is_section_start(line):
    """Проверяет, является ли строка началом секции"""
    line = line.strip()
    # Секция - это строка ВСЕМИ ЗАГЛАВНЫМИ, длиной более 10 символов
    # И не должна быть номером страницы или частью названия главы
    if len(line) < 10:
        return False
    # Все символы должны быть заглавными русскими буквами или пробелами
    if not re.match(r'^[А-Я\s]+$', line):
        return False
    # Не должна быть частью названия главы (содержать "ОСНОВЫ", "ПРОГРАММНЫХ" и т.д. в начале)
    if re.match(r'^(ОСНОВЫ|ПРОГРАММНЫХ|ПРЕДСТАВЛЕНИЯ|БАЗИС|ЯЗЫКА|ВИЗУАЛЬНОГО|ОРГАНИЗАЦИЯ|ПРОЦЕССА)', line):
        return False
    # Не должна быть "КОНТРОЛЬНЫЕ ВОПРОСЫ" или "ЗАКЛЮЧЕНИЕ" или "СПИСОК ЛИТЕРАТУРЫ"
    if line in ['КОНТРОЛЬНЫЕ ВОПРОСЫ', 'ЗАКЛЮЧЕНИЕ', 'СПИСОК ЛИТЕРАТУРЫ']:
        return False
    return True

def extract_chapters_and_sections(content):
    """Извлекает главы и секции из текста"""
    chapters = []
    lines = content.split('\n')
    i = 0
    
    # Пропускаем титульную часть до "ВВЕДЕНИЕ"
    while i < len(lines) and 'ВВЕДЕНИЕ' not in lines[i]:
        i += 1
    
    # Обрабатываем ВВЕДЕНИЕ
    if i < len(lines):
        intro_start = i
        intro_content = []
        i += 1
        
        # Ищем начало первой главы
        while i < len(lines):
            line = lines[i].strip()
            if is_chapter_start(line):
                break
            if line and not re.match(r'^[0-9]+$', line):  # Пропускаем номера страниц
                intro_content.append(lines[i])
            i += 1
        
        intro_text = clean_text('\n'.join(intro_content))
        if intro_text:
            chapters.append({
                'id': 'introduction',
                'title': 'Введение',
                'sections': [{
                    'id': 'introduction-1',
                    'title': 'Введение',
                    'content': intro_text
                }]
            })
    
    # Обрабатываем главы
    current_chapter = None
    current_section = None
    current_content = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Проверяем начало новой главы
        if is_chapter_start(line):
            # Сохраняем предыдущую секцию
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': clean_text('\n'.join(current_content))
                })
            
            # Начинаем новую главу
            chapter_match = re.match(r'^([0-9]+)\.\s+(.+)', line)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_title = chapter_match.group(2).strip()
                
                # Читаем полное название главы (может быть на нескольких строках)
                full_title = chapter_title
                i += 1
                # Читаем следующие строки, пока не встретим секцию или новую главу
                while i < len(lines):
                    next_line = lines[i].strip()
                    # Если следующая строка - начало секции или новой главы, останавливаемся
                    if is_section_start(next_line) or is_chapter_start(next_line):
                        break
                    # Если строка не пустая и не номер страницы, добавляем к названию
                    if next_line and not re.match(r'^[0-9]+$', next_line):
                        # Если строка вся заглавными и длинная, это может быть продолжение названия
                        if re.match(r'^[А-Я\s]+$', next_line) and len(next_line) > 5:
                            full_title += ' ' + next_line
                            i += 1
                        else:
                            # Это начало контента, останавливаемся
                            break
                    else:
                        i += 1
                
                current_chapter = {
                    'id': f'chapter-{chapter_num}',
                    'title': clean_text(full_title),
                    'sections': []
                }
                chapters.append(current_chapter)
                current_section = None
                current_content = []
                continue
        
        # Проверяем начало новой секции
        if current_chapter and is_section_start(line):
            # Сохраняем предыдущую секцию
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': clean_text('\n'.join(current_content))
                })
            
            # Начинаем новую секцию
            section_title = line
            # Создаем ID секции
            section_id = re.sub(r'[^А-Яа-я0-9]', '-', section_title.lower())
            section_id = re.sub(r'-+', '-', section_id).strip('-')
            section_id = f"{current_chapter['id']}-{section_id}"
            
            current_section = {
                'id': section_id,
                'title': section_title
            }
            current_content = []
            i += 1
            continue
        
        # Проверяем "КОНТРОЛЬНЫЕ ВОПРОСЫ" - это конец главы
        if line == 'КОНТРОЛЬНЫЕ ВОПРОСЫ':
            # Сохраняем предыдущую секцию
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': clean_text('\n'.join(current_content))
                })
            # Создаем секцию для контрольных вопросов
            questions_content = []
            i += 1
            # Читаем вопросы до следующей главы или конца
            while i < len(lines):
                next_line = lines[i].strip()
                if is_chapter_start(next_line) or next_line == 'ЗАКЛЮЧЕНИЕ':
                    break
                if next_line and not re.match(r'^[0-9]+$', next_line):
                    questions_content.append(lines[i])
                i += 1
            
            if questions_content:
                current_chapter['sections'].append({
                    'id': f"{current_chapter['id']}-контрольные-вопросы",
                    'title': 'Контрольные вопросы',
                    'content': clean_text('\n'.join(questions_content))
                })
            
            current_section = None
            current_content = []
            continue
        
        # Добавляем контент к текущей секции
        if current_section:
            if line and not re.match(r'^[0-9]+$', line):
                current_content.append(lines[i])
        elif current_chapter and not current_section:
            # Если есть глава, но нет секции, создаем первую секцию
            section_title = current_chapter['title']
            section_id = f"{current_chapter['id']}-1"
            current_section = {
                'id': section_id,
                'title': section_title
            }
            if line and not re.match(r'^[0-9]+$', line):
                current_content.append(lines[i])
        
        i += 1
    
    # Сохраняем последнюю секцию
    if current_section and current_content:
        current_chapter['sections'].append({
            'id': current_section['id'],
            'title': current_section['title'],
            'content': clean_text('\n'.join(current_content))
        })
    
    return chapters

def save_markdown_files(chapters, output_dir):
    """Сохраняет markdown файлы для каждой секции"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for chapter in chapters:
        for section in chapter['sections']:
            filename = f"{section['id']}.md"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {section['title']}\n\n")
                f.write(section['content'])
            
            # Сохраняем путь к файлу
            section['markdownFile'] = f"chapters/{filename}"
    
    total = sum(len(ch['sections']) for ch in chapters)
    print(f"Сохранено {total} markdown файлов в {output_dir}")

def generate_chapters_ts(chapters, output_file):
    """Генерирует chapters.ts файл"""
    lines = ["import { Chapter } from '../types';", "", "export const chapters: Chapter[] = ["]
    
    for chapter in chapters:
        lines.append("  {")
        lines.append(f"    id: '{chapter['id']}',")
        # Экранируем кавычки в названии
        title = chapter['title'].replace("'", "\\'")
        lines.append(f"    title: '{title}',")
        lines.append("    sections: [")
        
        for section in chapter['sections']:
            lines.append("      {")
            lines.append(f"        id: '{section['id']}',")
            # Экранируем кавычки в названии
            section_title = section['title'].replace("'", "\\'")
            lines.append(f"        title: '{section_title}',")
            lines.append(f"        markdownFile: '{section['markdownFile']}',")
            lines.append("      },")
        
        lines.append("    ],")
        lines.append("  },")
    
    lines.append("];")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Создан файл {output_file}")

def main():
    input_file = 'public/metod.txt'
    output_dir_public = 'public/content/chapters'
    output_dir_src = 'src/content/chapters'
    chapters_ts_file = 'src/data/chapters.ts'
    
    print("Читаю файл metod.txt...")
    content = read_file(input_file)
    
    print("Парсю главы и секции...")
    chapters = extract_chapters_and_sections(content)
    
    print(f"\nНайдено глав: {len(chapters)}")
    for ch in chapters:
        print(f"  - {ch['title']}: {len(ch['sections'])} секций")
        for sec in ch['sections']:
            print(f"      • {sec['title']}")
    
    print("\nСохраняю markdown файлы...")
    # Сохраняем в оба места
    save_markdown_files(chapters, output_dir_public)
    save_markdown_files(chapters, output_dir_src)
    
    print("\nГенерирую chapters.ts...")
    generate_chapters_ts(chapters, chapters_ts_file)
    
    print("\nГотово!")

if __name__ == '__main__':
    main()
