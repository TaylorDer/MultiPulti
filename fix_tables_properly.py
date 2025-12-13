#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Правильное преобразование таблиц с корректными заголовками
"""

import re

def parse_table_headers(lines, start_idx):
    """Парсит заголовки таблицы правильно"""
    i = start_idx
    headers = []
    
    # Пропускаем "Таблица X.Y"
    if i < len(lines) and re.match(r'^Таблица', lines[i], re.IGNORECASE):
        i += 1
    
    # Пропускаем пустые строки
    while i < len(lines) and not lines[i].strip():
        i += 1
    
    # Читаем строки заголовков (обычно 2-3 строки)
    header_lines = []
    while i < len(lines):
        line = lines[i].strip()
        if not line or '=== Страница' in line:
            i += 1
            continue
        if re.match(r'^Продолжение', line, re.IGNORECASE):
            break
        if re.match(r'^\d+', line):  # Начало данных
            break
        if line and line != '№':
            header_lines.append(line)
        i += 1
    
    # Парсим заголовки более умно
    if len(header_lines) >= 2:
        # Первая строка обычно "№" или "№ варианта"
        # Вторая строка - основные заголовки
        if header_lines[0].strip() == '№' or 'варианта' in header_lines[0]:
            headers.append('№ варианта')
        else:
            headers.append(header_lines[0])
        
        # Вторая строка содержит основные заголовки
        if len(header_lines) > 1:
            header_text = header_lines[1]
            # Разбиваем на колонки более умно
            # Ищем паттерны типа "С , %", "m, кг/с", "Т, °С"
            parts = re.split(r'\s+(?=[А-Яa-z])', header_text)
            for part in parts:
                part = part.strip()
                if part and part not in headers:
                    headers.append(part)
    
    return headers, i

def parse_table_data(lines, start_idx, num_cols):
    """Парсит данные таблицы"""
    i = start_idx
    rows = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Проверяем конец таблицы
        if re.match(r'^(Лабораторная|Практическая|КУРСОВАЯ|СПИСОК|Общие|Порядок|Содержание|Контрольные)', line, re.IGNORECASE):
            break
        
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            # Добавляем разделитель
            rows.append(['---'] * num_cols)
            i += 1
            # Пропускаем заголовки продолжения
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '№' or re.match(r'^[А-Я]', lines[i].strip())):
                i += 1
            continue
        
        # Парсим строку данных
        if re.match(r'^\d+', line):
            # Разбиваем на колонки
            parts = line.split()
            if len(parts) > 1:
                # Дополняем или обрезаем до нужного количества колонок
                row = parts[:num_cols]
                while len(row) < num_cols:
                    row.append('')
                rows.append(row)
        
        i += 1
    
    return rows, i

def create_markdown_table(title, headers, rows):
    """Создает правильно отформатированную Markdown таблицу"""
    if not headers or not rows:
        return ""
    
    result = []
    result.append(f'\n## {title}\n')
    result.append('')
    result.append('| ' + ' | '.join(headers) + ' |')
    result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    
    for row in rows:
        if row[0] == '---':
            # Разделитель для продолжения таблицы
            result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
        else:
            # Дополняем строку до нужного количества колонок
            row_data = row[:len(headers)]
            while len(row_data) < len(headers):
                row_data.append('')
            result.append('| ' + ' | '.join(row_data) + ' |')
    
    result.append('')
    return '\n'.join(result)

def main():
    print("Чтение extracted_text_full.txt...")
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    lines = full_text.split('\n')
    
    print("Парсинг таблиц...")
    tables = {}
    i = 0
    
    while i < len(lines):
        if re.match(r'^Таблица (\d+)\.(\d+)', lines[i], re.IGNORECASE):
            match = re.match(r'^Таблица (\d+)\.(\d+)', lines[i], re.IGNORECASE)
            table_key = f"{match.group(1)}.{match.group(2)}"
            table_title = lines[i].strip()
            
            print(f"\nПарсинг {table_title}...")
            
            # Парсим заголовки
            headers, data_start = parse_table_headers(lines, i)
            
            if not headers:
                print(f"  ⚠ Заголовки не найдены, используем упрощенный вариант")
                headers = ['№ варианта', 'Параметры']
            
            print(f"  Заголовки ({len(headers)}): {', '.join(headers[:5])}...")
            
            # Парсим данные
            rows, end_idx = parse_table_data(lines, data_start, len(headers))
            
            print(f"  Строк данных: {len(rows)}")
            
            if headers and rows:
                tables[table_key] = {
                    'title': table_title,
                    'headers': headers,
                    'rows': rows
                }
            
            i = end_idx
        else:
            i += 1
    
    print(f"\nНайдено таблиц: {len(tables)}")
    
    # Сохраняем примеры для проверки
    with open('tables_examples.txt', 'w', encoding='utf-8') as f:
        for key, table in list(tables.items())[:3]:
            f.write(f"\n{'='*60}\n")
            f.write(f"{table['title']}\n")
            f.write(f"Заголовки: {table['headers']}\n")
            f.write(f"Первые 3 строки:\n")
            for row in table['rows'][:3]:
                f.write(f"  {row}\n")
            f.write(f"\nMarkdown:\n")
            f.write(create_markdown_table(table['title'], table['headers'], table['rows'][:5]))
    
    print("Примеры сохранены в tables_examples.txt")
    
    # Обновляем chapters.ts
    print("\nОбновление chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
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
            continue
        
        print(f"Добавление таблицы {table_key} в {section_id}...")
        
        # Создаем Markdown таблицу
        md_table = create_markdown_table(table_data['title'], table_data['headers'], table_data['rows'])
        
        # Экранируем для TypeScript
        escaped_table = md_table.replace('\\', '\\\\')
        escaped_table = escaped_table.replace('`', '\\`')
        escaped_table = escaped_table.replace('${', '\\${')
        escaped_table = escaped_table.replace('\n', '\\n')
        
        # Удаляем старую таблицу и добавляем новую
        pattern = rf"(id: '{section_id}'[^`]*?content: `)([^`]*?)(`[,\)])"
        
        def replace_table(match):
            content = match.group(2)
            # Удаляем старую таблицу если есть
            content = re.sub(r'## Таблица \d+\.\d+.*?\| --- \|', '', content, flags=re.DOTALL)
            # Добавляем новую таблицу перед "Порядок выполнения работы" или в конец
            if 'Порядок выполнения работы' in content:
                content = content.replace('Порядок выполнения работы', escaped_table + 'Порядок выполнения работы')
            elif 'Содержание отчета' in content:
                content = content.replace('Содержание отчета', escaped_table + 'Содержание отчета')
            else:
                content = content + escaped_table
            return match.group(1) + content + match.group(3)
        
        new_ts = re.sub(pattern, replace_table, chapters_ts, flags=re.DOTALL)
        if new_ts != chapters_ts:
            chapters_ts = new_ts
            updated_count += 1
            print(f"  ✓ Обновлена")
    
    if updated_count > 0:
        print(f"\nСохранение... ({updated_count} таблиц обновлено)")
        with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
            f.write(chapters_ts)
        print("Готово!")
    else:
        print("Таблицы не обновлены.")

if __name__ == "__main__":
    main()

