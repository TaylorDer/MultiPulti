#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для парсинга Word документа и правильного разбиения на главы и подглавы
"""

import re
from pathlib import Path
from docx import Document

def read_word_document(filepath):
    """Читает Word документ и извлекает текст с сохранением структуры"""
    doc = Document(filepath)
    
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Определяем уровень заголовка по стилю
        style_name = para.style.name if para.style else ''
        is_heading = 'Heading' in style_name or 'Заголовок' in style_name
        
        # Определяем уровень
        level = 0
        if is_heading:
            match = re.search(r'Heading\s*(\d+)', style_name, re.IGNORECASE)
            if match:
                level = int(match.group(1))
        
        # Проверяем паттерны заголовков
        if not is_heading and not level:
            if re.match(r'^[0-9]+\.[\s]+[А-Я]', text):
                level = 1  # Глава
            elif re.match(r'^[0-9]+\.[0-9]+[\s]+[А-Я]', text):
                level = 2  # Подглава
            elif re.match(r'^[А-Я][А-Я\s]{15,}$', text) and len(text) > 20 and len(text) < 100:
                level = 2  # Заголовок ВСЕМИ ЗАГЛАВНЫМИ
        
        paragraphs.append({
            'text': text,
            'level': level,
            'is_heading': is_heading or level > 0,
            'style': style_name
        })
    
    return paragraphs

def is_table_of_contents(text):
    """Проверяет, является ли текст частью оглавления"""
    # Оглавление обычно содержит точки или табы перед номером страницы
    if re.match(r'^[А-Я].*[\.\t]+\s*[0-9]+$', text):
        return True
    # Или просто номер страницы в конце
    if re.search(r'\s+[0-9]+\s*$', text) and len(text) < 80:
        return True
    return False

def extract_chapters_and_sections(paragraphs):
    """Извлекает главы и секции из параграфов"""
    chapters = []
    current_chapter = None
    current_section = None
    current_content = []
    
    i = 0
    # Пропускаем титульную часть
    while i < len(paragraphs):
        para = paragraphs[i]
        text = para['text']
        
        # Ищем начало ВВЕДЕНИЯ или первой главы
        if text.upper() == 'ВВЕДЕНИЕ' or text == 'Введение' or re.match(r'^[0-9]+\.[\s]+[А-Я]', text):
            break
        i += 1
    
    # Обрабатываем ВВЕДЕНИЕ
    if i < len(paragraphs) and (paragraphs[i]['text'].upper() == 'ВВЕДЕНИЕ' or paragraphs[i]['text'] == 'Введение'):
        intro_content = []
        i += 1
        while i < len(paragraphs):
            next_para = paragraphs[i]
            next_text = next_para['text']
            if re.match(r'^[0-9]+\.[\s]+', next_text):
                break
            if next_text and not is_table_of_contents(next_text):
                intro_content.append(next_text)
            i += 1
        
        if intro_content:
            chapters.append({
                'id': 'introduction',
                'title': 'Введение',
                'sections': [{
                    'id': 'introduction-1',
                    'title': 'Введение',
                    'content': '\n\n'.join(intro_content).strip()
                }]
            })
    
    # Обрабатываем главы
    while i < len(paragraphs):
        para = paragraphs[i]
        text = para['text']
        level = para['level']
        
        # Пропускаем оглавление
        if is_table_of_contents(text):
            i += 1
            continue
        
        # Проверяем начало новой главы (паттерн "1. ОСНОВЫ...")
        chapter_match = re.match(r'^([1-4])\.\s+(.+)', text)
        if chapter_match:
            # Сохраняем предыдущую секцию
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': '\n\n'.join(current_content).strip()
                })
            
            # Начинаем новую главу
            chapter_num = chapter_match.group(1)
            chapter_title = chapter_match.group(2).strip()
            
            # Читаем полное название главы
            full_title = chapter_title
            i += 1
            while i < len(paragraphs):
                next_para = paragraphs[i]
                next_text = next_para['text']
                
                # Если оглавление - пропускаем
                if is_table_of_contents(next_text):
                    i += 1
                    continue
                
                # Если следующая строка - начало секции или новой главы, останавливаемся
                if (re.match(r'^[0-9]+\.[\s]+', next_text) or 
                    (next_para['level'] == 2 and next_text) or
                    (re.match(r'^[А-Я][А-Я\s]{15,}$', next_text) and len(next_text) > 15 and len(next_text) < 100)):
                    break
                
                # Если это продолжение названия (заглавные буквы, короткая строка)
                if re.match(r'^[А-Я\s]+$', next_text) and len(next_text) < 100 and not re.match(r'^[0-9]+$', next_text):
                    full_title += ' ' + next_text
                    i += 1
                else:
                    break
            
            current_chapter = {
                'id': f'chapter-{chapter_num}',
                'title': full_title.strip(),
                'sections': []
            }
            chapters.append(current_chapter)
            current_section = None
            current_content = []
            continue
        
        # Проверяем "КОНТРОЛЬНЫЕ ВОПРОСЫ"
        if text == 'КОНТРОЛЬНЫЕ ВОПРОСЫ':
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': '\n\n'.join(current_content).strip()
                })
            
            questions_content = []
            i += 1
            while i < len(paragraphs):
                next_para = paragraphs[i]
                next_text = next_para['text']
                if re.match(r'^[0-9]+\.[\s]+', next_text) or next_text == 'ЗАКЛЮЧЕНИЕ':
                    break
                if next_text and not is_table_of_contents(next_text):
                    questions_content.append(next_text)
                i += 1
            
            if questions_content:
                current_chapter['sections'].append({
                    'id': f"{current_chapter['id']}-контрольные-вопросы",
                    'title': 'Контрольные вопросы',
                    'content': '\n\n'.join(questions_content).strip()
                })
            
            current_section = None
            current_content = []
            continue
        
        # Проверяем "ЗАКЛЮЧЕНИЕ"
        if text == 'ЗАКЛЮЧЕНИЕ':
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': '\n\n'.join(current_content).strip()
                })
            
            conclusion_content = []
            i += 1
            while i < len(paragraphs):
                next_para = paragraphs[i]
                next_text = next_para['text']
                if next_text == 'СПИСОК ЛИТЕРАТУРЫ':
                    break
                if next_text and not is_table_of_contents(next_text):
                    conclusion_content.append(next_text)
                i += 1
            
            if conclusion_content:
                chapters.append({
                    'id': 'conclusion',
                    'title': 'Заключение',
                    'sections': [{
                        'id': 'conclusion-1',
                        'title': 'Заключение',
                        'content': '\n\n'.join(conclusion_content).strip()
                    }]
                })
            
            current_chapter = None
            current_section = None
            current_content = []
            continue
        
        # Проверяем начало новой секции (уровень 2 или заголовок ВСЕМИ ЗАГЛАВНЫМИ)
        if current_chapter and (level == 2 or (re.match(r'^[А-Я][А-Я\s]{15,}$', text) and len(text) > 15 and len(text) < 100)):
            # Игнорируем служебные заголовки
            if text in ['СОДЕРЖАНИЕ', 'СПИСОК ЛИТЕРАТУРЫ']:
                i += 1
                continue
            
            # Сохраняем предыдущую секцию
            if current_section and current_content:
                current_chapter['sections'].append({
                    'id': current_section['id'],
                    'title': current_section['title'],
                    'content': '\n\n'.join(current_content).strip()
                })
            
            # Начинаем новую секцию
            section_title = text
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
        
        # Добавляем контент к текущей секции
        if current_section:
            if text and not is_table_of_contents(text):
                current_content.append(text)
        elif current_chapter and not current_section:
            # Если есть глава, но нет секции, создаем первую секцию
            section_title = current_chapter['title']
            section_id = f"{current_chapter['id']}-1"
            current_section = {
                'id': section_id,
                'title': section_title
            }
            if text and not is_table_of_contents(text):
                current_content.append(text)
        
        i += 1
    
    # Сохраняем последнюю секцию
    if current_section and current_content:
        current_chapter['sections'].append({
            'id': current_section['id'],
            'title': current_section['title'],
            'content': '\n\n'.join(current_content).strip()
        })
    
    return chapters

def clean_text(text):
    """Очищает текст от лишних символов"""
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def save_markdown_files(chapters, output_dir):
    """Сохраняет markdown файлы для каждой секции"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for chapter in chapters:
        for section in chapter['sections']:
            filename = f"{section['id']}.md"
            filepath = output_path / filename
            
            content = clean_text(section['content'])
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {section['title']}\n\n")
                f.write(content)
            
            section['markdownFile'] = f"chapters/{filename}"
    
    total = sum(len(ch['sections']) for ch in chapters)
    print(f"Сохранено {total} markdown файлов в {output_dir}")

def generate_chapters_ts(chapters, output_file):
    """Генерирует chapters.ts файл"""
    lines = ["import { Chapter } from '../types';", "", "export const chapters: Chapter[] = ["]
    
    for chapter in chapters:
        lines.append("  {")
        lines.append(f"    id: '{chapter['id']}',")
        title = chapter['title'].replace("'", "\\'")
        lines.append(f"    title: '{title}',")
        lines.append("    sections: [")
        
        for section in chapter['sections']:
            lines.append("      {")
            lines.append(f"        id: '{section['id']}',")
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
    input_file = 'public/milovanov-t.docx'
    output_dir_public = 'public/content/chapters'
    output_dir_src = 'src/content/chapters'
    chapters_ts_file = 'src/data/chapters.ts'
    
    print("Читаю Word документ...")
    paragraphs = read_word_document(input_file)
    print(f"Прочитано {len(paragraphs)} параграфов")
    
    print("\nПарсю главы и секции...")
    chapters = extract_chapters_and_sections(paragraphs)
    
    print(f"\nНайдено глав: {len(chapters)}")
    for ch in chapters:
        print(f"  - {ch['title']}: {len(ch['sections'])} секций")
        for sec in ch['sections'][:3]:
            print(f"      • {sec['title']}")
        if len(ch['sections']) > 3:
            print(f"      ... и еще {len(ch['sections']) - 3} секций")
    
    print("\nСохраняю markdown файлы...")
    save_markdown_files(chapters, output_dir_public)
    save_markdown_files(chapters, output_dir_src)
    
    print("\nГенерирую chapters.ts...")
    generate_chapters_ts(chapters, chapters_ts_file)
    
    print("\nГотово!")

if __name__ == '__main__':
    main()
