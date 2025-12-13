#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальный скрипт для парсинга metod.txt и разбиения на главы и секции
Использует точные позиции глав
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

def extract_chapters_and_sections(content):
    """Извлекает главы и секции из текста"""
    chapters = []
    lines = content.split('\n')
    
    # Находим позиции глав
    chapter_starts = {}
    for i, line in enumerate(lines):
        if '1. ОСНОВЫ ПРОЕКТИРОВАНИЯ' in line:
            chapter_starts[1] = i
        elif '2. ОСНОВЫ ОБЪЕКТНО-ОРИЕНТИРОВАННОГО' in line:
            chapter_starts[2] = i
        elif '3. БАЗИС ЯЗЫКА' in line:
            chapter_starts[3] = i
        elif '4. ОРГАНИЗАЦИЯ ПРОЦЕССА КОНСТРУИРОВАНИЯ' in line:
            chapter_starts[4] = i
        elif 'ВВЕДЕНИЕ' in line and 'introduction' not in chapter_starts:
            chapter_starts['introduction'] = i
        elif 'ЗАКЛЮЧЕНИЕ' in line and 'conclusion' not in chapter_starts:
            chapter_starts['conclusion'] = i
    
    # Обрабатываем ВВЕДЕНИЕ
    if 'introduction' in chapter_starts:
        intro_start = chapter_starts['introduction']
        intro_end = chapter_starts.get(1, len(lines))
        intro_content = []
        for i in range(intro_start + 1, intro_end):
            line = lines[i].strip()
            if line and not re.match(r'^[0-9]+$', line):
                intro_content.append(lines[i])
        
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
    
    # Обрабатываем основные главы (1-4)
    for chapter_num in [1, 2, 3, 4]:
        if chapter_num not in chapter_starts:
            continue
        
        start_idx = chapter_starts[chapter_num]
        # Определяем конец главы (начало следующей или "КОНТРОЛЬНЫЕ ВОПРОСЫ")
        end_idx = len(lines)
        if chapter_num < 4:
            end_idx = chapter_starts.get(chapter_num + 1, len(lines))
        else:
            # Для последней главы ищем "ЗАКЛЮЧЕНИЕ"
            end_idx = chapter_starts.get('conclusion', len(lines))
        
        # Извлекаем название главы
        chapter_title_lines = []
        i = start_idx
        while i < end_idx and i < len(lines):
            line = lines[i].strip()
            # Если это начало главы
            if re.match(r'^[1-4]\.\s+', line):
                chapter_title_lines.append(line)
                i += 1
                # Читаем продолжение названия
                while i < end_idx and i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line or re.match(r'^[0-9]+$', next_line):
                        i += 1
                        continue
                    # Если следующая строка - заголовок секции (все заглавные, длинная)
                    if re.match(r'^[А-Я][А-Я\s]{15,}$', next_line):
                        break
                    # Если следующая строка - начало новой главы
                    if re.match(r'^[1-4]\.\s+', next_line):
                        break
                    # Если это продолжение названия (заглавные буквы)
                    if re.match(r'^[А-Я\s]+$', next_line) and len(next_line) > 5:
                        chapter_title_lines.append(next_line)
                        i += 1
                    else:
                        break
                break
            i += 1
        
        chapter_title = ' '.join([l.replace(f'{chapter_num}.', '').strip() for l in chapter_title_lines]).strip()
        
        # Извлекаем секции
        sections = []
        current_section = None
        current_content = []
        in_questions = False
        
        i = start_idx
        while i < end_idx:
            line = lines[i].strip()
            
            # Проверяем "КОНТРОЛЬНЫЕ ВОПРОСЫ"
            if line == 'КОНТРОЛЬНЫЕ ВОПРОСЫ':
                # Сохраняем предыдущую секцию
                if current_section and current_content:
                    sections.append({
                        'id': current_section['id'],
                        'title': current_section['title'],
                        'content': clean_text('\n'.join(current_content))
                    })
                
                # Создаем секцию для контрольных вопросов
                questions_content = []
                i += 1
                while i < end_idx:
                    next_line = lines[i].strip()
                    if re.match(r'^[1-4]\.\s+', next_line) or next_line == 'ЗАКЛЮЧЕНИЕ':
                        break
                    if next_line and not re.match(r'^[0-9]+$', next_line):
                        questions_content.append(lines[i])
                    i += 1
                
                if questions_content:
                    sections.append({
                        'id': f"chapter-{chapter_num}-контрольные-вопросы",
                        'title': 'Контрольные вопросы',
                        'content': clean_text('\n'.join(questions_content))
                    })
                
                current_section = None
                current_content = []
                continue
            
            # Пропускаем строки с номерами глав
            if re.match(r'^[1-4]\.\s+', line):
                # Это начало главы, пропускаем название
                i += 1
                # Пропускаем продолжение названия
                while i < end_idx:
                    next_line = lines[i].strip()
                    if not next_line or re.match(r'^[0-9]+$', next_line):
                        i += 1
                        continue
                    if re.match(r'^[А-Я][А-Я\s]{15,}$', next_line):
                        break
                    if re.match(r'^[1-4]\.\s+', next_line):
                        break
                    if re.match(r'^[А-Я\s]+$', next_line) and len(next_line) > 5:
                        i += 1
                    else:
                        break
                continue
            
            # Проверяем начало новой секции (заголовок ВСЕМИ ЗАГЛАВНЫМИ, длиной > 15)
            if re.match(r'^[А-Я][А-Я\s]{15,}$', line) and line not in ['КОНТРОЛЬНЫЕ ВОПРОСЫ', 'ЗАКЛЮЧЕНИЕ', 'СПИСОК ЛИТЕРАТУРЫ']:
                # Сохраняем предыдущую секцию
                if current_section and current_content:
                    sections.append({
                        'id': current_section['id'],
                        'title': current_section['title'],
                        'content': clean_text('\n'.join(current_content))
                    })
                
                # Начинаем новую секцию
                section_title = line
                section_id = re.sub(r'[^А-Яа-я0-9]', '-', section_title.lower())
                section_id = re.sub(r'-+', '-', section_id).strip('-')
                section_id = f"chapter-{chapter_num}-{section_id}"
                
                current_section = {
                    'id': section_id,
                    'title': section_title
                }
                current_content = []
                i += 1
                continue
            
            # Добавляем контент к текущей секции
            if current_section:
                if line and not re.match(r'^[0-9]+$', line):
                    current_content.append(lines[i])
            elif not current_section:
                # Если нет секции, создаем первую
                section_title = chapter_title
                section_id = f"chapter-{chapter_num}-1"
                current_section = {
                    'id': section_id,
                    'title': section_title
                }
                if line and not re.match(r'^[0-9]+$', line):
                    current_content.append(lines[i])
            
            i += 1
        
        # Сохраняем последнюю секцию
        if current_section and current_content:
            sections.append({
                'id': current_section['id'],
                'title': current_section['title'],
                'content': clean_text('\n'.join(current_content))
            })
        
        if sections:
            chapters.append({
                'id': f'chapter-{chapter_num}',
                'title': chapter_title,
                'sections': sections
            })
    
    # Обрабатываем ЗАКЛЮЧЕНИЕ
    if 'conclusion' in chapter_starts:
        concl_start = chapter_starts['conclusion']
        concl_content = []
        i = concl_start + 1
        while i < len(lines):
            line = lines[i].strip()
            if line == 'СПИСОК ЛИТЕРАТУРЫ':
                break
            if line and not re.match(r'^[0-9]+$', line):
                concl_content.append(lines[i])
            i += 1
        
        if concl_content:
            chapters.append({
                'id': 'conclusion',
                'title': 'Заключение',
                'sections': [{
                    'id': 'conclusion-1',
                    'title': 'Заключение',
                    'content': clean_text('\n'.join(concl_content))
                }]
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
        for sec in ch['sections'][:3]:  # Показываем первые 3 секции
            print(f"      • {sec['title']}")
        if len(ch['sections']) > 3:
            print(f"      ... и еще {len(ch['sections']) - 3} секций")
    
    print("\nСохраняю markdown файлы...")
    # Сохраняем в оба места
    save_markdown_files(chapters, output_dir_public)
    save_markdown_files(chapters, output_dir_src)
    
    print("\nГенерирую chapters.ts...")
    generate_chapters_ts(chapters, chapters_ts_file)
    
    print("\nГотово!")

if __name__ == '__main__':
    main()

