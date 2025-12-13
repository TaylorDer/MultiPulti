#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенное преобразование таблиц в Markdown формат
"""

import re

def parse_table_section(lines, start_idx):
    """Парсит таблицу из строк"""
    result = []
    i = start_idx
    
    # Пропускаем заголовок "Таблица X.Y"
    if i < len(lines) and re.match(r'^Таблица \d+\.\d+', lines[i], re.IGNORECASE):
        result.append(f'\n## {lines[i].strip()}\n')
        i += 1
    
    # Пропускаем пустые строки
    while i < len(lines) and not lines[i].strip():
        i += 1
    
    # Собираем заголовки (обычно 2-3 строки до первой строки с данными)
    header_lines = []
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            result.append(f'\n*{line}*\n')
            i += 1
            # Пропускаем пустые и заголовки продолжения
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '№' or re.match(r'^[А-Я]', lines[i].strip())):
                i += 1
            continue
        if re.match(r'^\d+', line):  # Начало данных
            break
        if line and line != '№':
            header_lines.append(line)
        i += 1
    
    # Формируем заголовки таблицы
    if header_lines:
        # Объединяем заголовки в одну строку
        header_text = ' '.join(header_lines)
        # Разбиваем на колонки (приблизительно по пробелам)
        headers = ['№ варианта']
        # Добавляем остальные колонки из заголовка
        parts = header_text.split()
        for part in parts:
            if part and part not in ['варианта', '№']:
                headers.append(part)
        
        # Создаем Markdown таблицу
        result.append('| ' + ' | '.join(headers[:15]) + ' |')  # Ограничиваем количество колонок
        result.append('| ' + ' | '.join(['---'] * min(len(headers), 15)) + ' |')
    
    # Читаем данные
    while i < len(lines):
        line = lines[i].strip()
        
        # Проверяем конец таблицы
        if re.match(r'^(Лабораторная|Практическая|КУРСОВАЯ|СПИСОК|Общие|Порядок|Содержание|Контрольные)', line, re.IGNORECASE):
            break
        
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            result.append(f'\n*{line}*\n')
            i += 1
            # Пропускаем заголовки продолжения
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '№' or re.match(r'^[А-Я]', lines[i].strip())):
                i += 1
            continue
        
        # Парсим строку данных
        if re.match(r'^\d+', line):
            parts = line.split()
            if len(parts) > 1:
                # Ограничиваем количество колонок
                row_parts = parts[:15]
                result.append('| ' + ' | '.join(row_parts) + ' |')
        
        i += 1
    
    result.append('')  # Пустая строка после таблицы
    return '\n'.join(result), i

def convert_tables_in_text(text):
    """Преобразует все таблицы в тексте"""
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Ищем начало таблицы
        if re.match(r'^Таблица \d+\.\d+', line, re.IGNORECASE):
            table_md, new_i = parse_table_section(lines, i)
            result.append(table_md)
            i = new_i
        else:
            result.append(line)
            i += 1
    
    return '\n'.join(result)

def main():
    print("Чтение chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Находим все content блоки
    pattern = r"(content: `)(.*?)(`[,\)])"
    
    def convert_content(match):
        content = match.group(2)
        # Распаковываем
        content = content.replace('\\n', '\n')
        # Преобразуем таблицы
        content = convert_tables_in_text(content)
        # Упаковываем обратно
        content = content.replace('\n', '\\n')
        content = content.replace('`', '\\`')
        content = content.replace('${', '\\${')
        return match.group(1) + content + match.group(3)
    
    new_chapters_ts = re.sub(pattern, convert_content, chapters_ts, flags=re.DOTALL)
    
    print("Сохранение...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(new_chapters_ts)
    
    print("Готово! Таблицы преобразованы.")

if __name__ == "__main__":
    main()

