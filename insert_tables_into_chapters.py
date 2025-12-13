#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Вставка таблиц в chapters.ts
"""

import re
import json

def create_markdown_table(headers, rows):
    """Создает Markdown таблицу"""
    if not headers or not rows:
        return ""
    
    # Ограничиваем количество колонок
    max_cols = min(12, len(headers))
    headers = headers[:max_cols]
    
    result = []
    result.append('\n| ' + ' | '.join(headers) + ' |')
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
    
    if i < len(text_lines) and re.match(r'^Таблица \d+\.\d+', text_lines[i], re.IGNORECASE):
        table_title = text_lines[i].strip()
        i += 1
    
    while i < len(text_lines) and not text_lines[i].strip():
        i += 1
    
    header_lines = []
    while i < len(text_lines):
        line = text_lines[i].strip()
        if not line or '=== Страница' in line:
            i += 1
            continue
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            rows.append(['*Продолжение таблицы*'] + [''] * 10)
            i += 1
            while i < len(text_lines) and (not text_lines[i].strip() or text_lines[i].strip() == '№' or re.match(r'^[А-Я]', text_lines[i].strip())):
                i += 1
            continue
        if re.match(r'^\d+', line):
            break
        if line and line != '№':
            header_lines.append(line)
        i += 1
    
    if header_lines:
        header_text = ' '.join(header_lines)
        parts = header_text.split()
        headers = ['№ варианта']
        for part in parts:
            if part and part not in ['варианта', '№']:
                if len(headers) < 12:
                    headers.append(part)
    
    while i < len(text_lines):
        line = text_lines[i].strip()
        
        if re.match(r'^(Лабораторная|Практическая|КУРСОВАЯ|СПИСОК|Общие|Порядок|Содержание|Контрольные)', line, re.IGNORECASE):
            break
        
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            rows.append(['*Продолжение таблицы*'] + [''] * 10)
            i += 1
            while i < len(text_lines) and (not text_lines[i].strip() or text_lines[i].strip() == '№' or re.match(r'^[А-Я]', text_lines[i].strip())):
                i += 1
            continue
        
        if re.match(r'^\d+', line):
            parts = line.split()
            if len(parts) > 1:
                rows.append(parts[:12])
        
        i += 1
    
    return table_title, headers, rows, i

def main():
    print("Чтение extracted_text_full.txt...")
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    lines = full_text.split('\n')
    
    print("Поиск и парсинг таблиц...")
    tables = {}
    i = 0
    while i < len(lines):
        if re.match(r'^Таблица (\d+)\.(\d+)', lines[i], re.IGNORECASE):
            match = re.match(r'^Таблица (\d+)\.(\d+)', lines[i], re.IGNORECASE)
            table_key = f"{match.group(1)}.{match.group(2)}"
            title, headers, rows, new_i = parse_table_from_text(lines, i)
            if headers and rows:
                tables[table_key] = {
                    'title': title,
                    'headers': headers,
                    'rows': rows
                }
                print(f"  {title}: {len(rows)} строк")
            i = new_i
        else:
            i += 1
    
    print(f"\nНайдено таблиц: {len(tables)}")
    
    print("Чтение chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Маппинг таблиц к секциям
    table_to_section = {
        '1.1': 'chapter1-lab1',
        '1.2': 'chapter1-lab2',
        '1.3': 'chapter1-lab3',
        '1.4': 'chapter1-lab4',
        '1.5': 'chapter1-lab5',
        '1.6': 'chapter1-lab6',
        '2.1': 'chapter2-lab1',
        '2.2': 'chapter2-lab2',
        '2.3': 'chapter2-lab3',
        '2.4': 'chapter2-lab4',
        '2.5': 'chapter2-lab5',
        '3.1': 'chapter3-practice1',
    }
    
    updated_count = 0
    for table_key, table_data in tables.items():
        section_id = table_to_section.get(table_key)
        if not section_id:
            print(f"  Пропущена таблица {table_key} (нет маппинга)")
            continue
        
        print(f"\nДобавление таблицы {table_key} в {section_id}...")
        
        # Создаем Markdown таблицу
        md_table = create_markdown_table(table_data['headers'], table_data['rows'])
        table_block = f"\n## {table_data['title']}\n{md_table}\n"
        
        # Экранируем для TypeScript
        escaped_table = table_block.replace('\\', '\\\\')
        escaped_table = escaped_table.replace('`', '\\`')
        escaped_table = escaped_table.replace('${', '\\${')
        escaped_table = escaped_table.replace('\n', '\\n')
        
        # Ищем секцию и добавляем таблицу перед "Порядок выполнения работы" или в конец
        pattern = rf"(id: '{section_id}'[^`]*?content: `)([^`]*?)(`[,\)])"
        
        def add_table(match):
            content = match.group(2)
            # Добавляем таблицу перед "Порядок выполнения работы" или в конец
            if 'Порядок выполнения работы' in content:
                content = content.replace('Порядок выполнения работы', escaped_table + 'Порядок выполнения работы')
            elif 'Содержание отчета' in content:
                content = content.replace('Содержание отчета', escaped_table + 'Содержание отчета')
            else:
                content = content + escaped_table
            return match.group(1) + content + match.group(3)
        
        new_ts = re.sub(pattern, add_table, chapters_ts, flags=re.DOTALL)
        if new_ts != chapters_ts:
            chapters_ts = new_ts
            updated_count += 1
            print(f"  ✓ Добавлена")
        else:
            print(f"  ✗ Секция не найдена")
    
    if updated_count > 0:
        print(f"\nСохранение... ({updated_count} таблиц добавлено)")
        with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
            f.write(chapters_ts)
        print("Готово!")
    else:
        print("\nТаблицы не добавлены.")

if __name__ == "__main__":
    main()

