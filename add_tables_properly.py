#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Правильное добавление таблиц в chapters.ts
"""

import re

def create_markdown_table(headers, rows):
    """Создает Markdown таблицу"""
    if not headers or not rows:
        return ""
    
    # Ограничиваем количество колонок для читаемости
    max_cols = 12
    headers = headers[:max_cols]
    
    result = []
    result.append('| ' + ' | '.join(headers) + ' |')
    result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    
    for row in rows:
        row_data = row[:max_cols]
        # Дополняем до нужного количества колонок
        while len(row_data) < len(headers):
            row_data.append('')
        result.append('| ' + ' | '.join(row_data) + ' |')
    
    return '\n'.join(result)

def parse_table_from_text(text_lines, start_idx):
    """Парсит таблицу из текста"""
    i = start_idx
    table_title = ""
    headers = []
    rows = []
    
    # Читаем заголовок таблицы
    if i < len(text_lines) and re.match(r'^Таблица \d+\.\d+', text_lines[i], re.IGNORECASE):
        table_title = text_lines[i].strip()
        i += 1
    
    # Пропускаем пустые строки
    while i < len(text_lines) and not text_lines[i].strip():
        i += 1
    
    # Читаем заголовки (обычно 2-3 строки)
    header_lines = []
    while i < len(text_lines):
        line = text_lines[i].strip()
        if not line or line == '=== Страница':
            i += 1
            continue
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            # Продолжение таблицы - добавляем разделитель
            rows.append(['---', '---', '---'])
            i += 1
            # Пропускаем заголовки продолжения
            while i < len(text_lines) and (not text_lines[i].strip() or text_lines[i].strip() == '№' or re.match(r'^[А-Я]', text_lines[i].strip())):
                i += 1
            continue
        if re.match(r'^\d+', line):  # Начало данных
            break
        if line and line != '№':
            header_lines.append(line)
        i += 1
    
    # Формируем заголовки
    if header_lines:
        # Объединяем заголовки
        header_text = ' '.join(header_lines)
        # Разбиваем на слова
        parts = header_text.split()
        headers = ['№ варианта']
        # Добавляем остальные колонки (упрощенно)
        for part in parts:
            if part and part not in ['варианта', '№']:
                if len(headers) < 12:  # Ограничиваем количество колонок
                    headers.append(part)
    
    # Читаем данные
    while i < len(text_lines):
        line = text_lines[i].strip()
        
        # Проверяем конец таблицы
        if re.match(r'^(Лабораторная|Практическая|КУРСОВАЯ|СПИСОК|Общие|Порядок|Содержание|Контрольные)', line, re.IGNORECASE):
            break
        
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            rows.append(['---', '---', '---'])
            i += 1
            while i < len(text_lines) and (not text_lines[i].strip() or text_lines[i].strip() == '№' or re.match(r'^[А-Я]', text_lines[i].strip())):
                i += 1
            continue
        
        # Парсим строку данных
        if re.match(r'^\d+', line):
            parts = line.split()
            if len(parts) > 1:
                rows.append(parts[:12])  # Ограничиваем количество колонок
        
        i += 1
    
    return table_title, headers, rows, i

def main():
    print("Чтение extracted_text_full.txt...")
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    lines = full_text.split('\n')
    
    print("Поиск таблиц...")
    tables_data = []
    i = 0
    while i < len(lines):
        if re.match(r'^Таблица \d+\.\d+', lines[i], re.IGNORECASE):
            title, headers, rows, new_i = parse_table_from_text(lines, i)
            if headers and rows:
                tables_data.append({
                    'title': title,
                    'headers': headers,
                    'rows': rows
                })
                print(f"Найдена таблица: {title} ({len(rows)} строк)")
            i = new_i
        else:
            i += 1
    
    print(f"\nНайдено таблиц: {len(tables_data)}")
    
    # Сохраняем информацию о таблицах
    with open('tables_info.txt', 'w', encoding='utf-8') as f:
        for table in tables_data:
            f.write(f"\n{table['title']}\n")
            f.write(f"Заголовки: {', '.join(table['headers'])}\n")
            f.write(f"Строк: {len(table['rows'])}\n")
            f.write(f"Первые 3 строки:\n")
            for row in table['rows'][:3]:
                f.write(f"  {row}\n")
    
    print("Информация о таблицах сохранена в tables_info.txt")
    print("\nДля добавления таблиц в chapters.ts нужно:")
    print("1. Найти соответствующие секции в chapters.ts")
    print("2. Добавить Markdown таблицы в content блоки")

if __name__ == "__main__":
    main()

