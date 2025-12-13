#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создание идеально отформатированных таблиц с правильными заголовками
"""

import re

def parse_table_structure(lines, start_idx):
    """Парсит структуру таблицы с многострочными заголовками"""
    i = start_idx
    
    # Пропускаем "Таблица X.Y"
    table_title = ""
    if i < len(lines) and re.match(r'^Таблица', lines[i], re.IGNORECASE):
        table_title = lines[i].strip()
        i += 1
    
    # Пропускаем пустые строки
    while i < len(lines) and not lines[i].strip():
        i += 1
    
    # Собираем строки заголовков
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
        if line:
            header_lines.append(line)
        i += 1
    
    # Парсим заголовки правильно
    headers = []
    
    if len(header_lines) >= 3:
        # Строка 1: "№"
        # Строка 2: основные заголовки "С , % С , % С , % m, кг/с m, кг/c m , кг/с Т, °С Т, °С Т , °С"
        # Строка 3: подзаголовки "варианта 0 1 вх 0 1 вх 0 1 п"
        
        main_header = header_lines[-2]  # Основные заголовки
        sub_header = header_lines[-1]    # Подзаголовки
        
        # Разбиваем на колонки
        # Сначала "№ варианта"
        if header_lines[0].strip() == '№' and 'варианта' in sub_header:
            headers.append('№ варианта')
            sub_parts = sub_header.split()
            main_parts = main_header.split()
            
            # Парсим остальные колонки
            # Ищем паттерны в main_header и объединяем с sub_header
            col_patterns = [
                (r'С\s*,\s*%', 'С'),
                (r'm\s*,\s*кг/с', 'm'),
                (r'm\s*,\s*кг/c', 'm'),
                (r'Т\s*,\s*°С', 'Т'),
            ]
            
            # Упрощенный подход: разбиваем sub_header и объединяем с main_header
            sub_words = sub_header.split()
            main_words = main_header.split()
            
            # Создаем заголовки на основе количества подзаголовков
            col_idx = 0
            for sub_word in sub_words:
                if sub_word == 'варианта':
                    continue  # Уже обработали
                
                # Ищем соответствующий паттерн в main_header
                if col_idx < len(main_words):
                    main_part = main_words[col_idx]
                    # Объединяем
                    header = f"{main_part} {sub_word}"
                    headers.append(header)
                    col_idx += 1
                else:
                    headers.append(sub_word)
        else:
            # Упрощенный вариант
            headers = ['№ варианта']
            if len(header_lines) >= 2:
                # Берем последнюю строку заголовков и разбиваем
                last_header = header_lines[-1]
                parts = last_header.split()
                headers.extend(parts[:10])  # Ограничиваем количество
    
    # Если не удалось распарсить
    if len(headers) < 2:
        # Используем данные из первой строки для определения количества колонок
        if i < len(lines) and re.match(r'^\d+', lines[i]):
            first_row = lines[i].split()
            num_cols = len(first_row)
            headers = ['№ варианта'] + [f'Параметр {j+1}' for j in range(num_cols - 1)]
    
    return table_title, headers, i

def parse_table_rows(lines, start_idx, num_cols):
    """Парсит строки данных таблицы"""
    i = start_idx
    rows = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        if re.match(r'^(Лабораторная|Практическая|КУРСОВАЯ|СПИСОК|Общие|Порядок|Содержание|Контрольные)', line, re.IGNORECASE):
            break
        
        if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
            rows.append(['*Продолжение*'] + [''] * (num_cols - 1))
            i += 1
            # Пропускаем заголовки продолжения
            while i < len(lines) and (not lines[i].strip() or lines[i].strip() == '№' or re.match(r'^[А-Я]', lines[i].strip())):
                i += 1
            continue
        
        if re.match(r'^\d+', line):
            parts = line.split()
            if len(parts) > 1:
                row = parts[:num_cols]
                while len(row) < num_cols:
                    row.append('')
                rows.append(row)
        
        i += 1
    
    return rows, i

def create_markdown_table(title, headers, rows):
    """Создает Markdown таблицу"""
    if not headers or not rows:
        return ""
    
    result = []
    result.append(f'\n## {title}\n')
    result.append('')
    result.append('| ' + ' | '.join(headers) + ' |')
    result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    
    for row in rows:
        if row[0] == '*Продолжение*':
            result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
        else:
            row_data = row[:len(headers)]
            while len(row_data) < len(headers):
                row_data.append('')
            result.append('| ' + ' | '.join(row_data) + ' |')
    
    result.append('')
    return '\n'.join(result)

# Специальные заголовки для известных таблиц
TABLE_HEADERS = {
    '1.1': ['№ варианта', 'С₀ %', 'С₁ %', 'Свх %', 'm₀ кг/с', 'm₁ кг/с', 'mвх кг/с', 'Т₀ °С', 'Т₁ °С', 'Тп °С'],
    '1.2': ['№ варианта', '∆Cвх %', '∆mвх кг/с', '∆Tп °С'],
    '1.3': ['№ варианта', 'm кг/с', 'Свх %', 'L м', 'Т₀ К', 'Т₁ К'],
    '2.1': ['№ варианта', 'f(X)', 'a', 'b'],
    '2.2': ['№ варианта', 'f(X)', 'a', 'b', 'ε'],
    '3.1': ['№ варианта', 'Функционал', 'Граничные условия'],
}

def main():
    print("Чтение extracted_text_full.txt...")
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    lines = full_text.split('\n')
    
    print("Парсинг таблиц...")
    tables = {}
    i = 0
    
    while i < len(lines):
        match = re.match(r'^Таблица (\d+)\.(\d+)', lines[i], re.IGNORECASE)
        if match:
            table_key = f"{match.group(1)}.{match.group(2)}"
            table_title, headers, data_start = parse_table_structure(lines, i)
            
            # Используем специальные заголовки если есть
            if table_key in TABLE_HEADERS:
                headers = TABLE_HEADERS[table_key]
                print(f"{table_title}: используем предопределенные заголовки")
            else:
                print(f"{table_title}: {len(headers)} заголовков")
            
            # Парсим данные
            rows, end_idx = parse_table_rows(lines, data_start, len(headers))
            
            print(f"  Строк данных: {len(rows)}")
            
            tables[table_key] = {
                'title': table_title,
                'headers': headers,
                'rows': rows
            }
            
            i = end_idx
        else:
            i += 1
    
    print(f"\nНайдено таблиц: {len(tables)}")
    
    # Обновляем chapters.ts
    print("\nОбновление chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    table_to_section = {
        '1.1': 'chapter1-lab1', '1.2': 'chapter1-lab2', '1.3': 'chapter1-lab3',
        '1.4': 'chapter1-lab4', '1.5': 'chapter1-lab5', '1.6': 'chapter1-lab6',
        '2.1': 'chapter2-lab1', '2.2': 'chapter2-lab2', '2.3': 'chapter2-lab3',
        '2.4': 'chapter2-lab4', '2.5': 'chapter2-lab5',
        '3.1': 'chapter3-practice1',
    }
    
    for table_key, table_data in tables.items():
        section_id = table_to_section.get(table_key)
        if not section_id:
            continue
        
        md_table = create_markdown_table(table_data['title'], table_data['headers'], table_data['rows'])
        escaped_table = md_table.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${').replace('\n', '\\n')
        
        pattern = rf"(id: '{section_id}'[^`]*?content: `)([^`]*?)(`[,\)])"
        
        def replace_table(match):
            content = match.group(2)
            # Удаляем старую таблицу
            content = re.sub(r'## Таблица \d+\.\d+.*?\| --- \|.*?\|', '', content, flags=re.DOTALL)
            # Добавляем новую
            if 'Порядок выполнения работы' in content:
                content = content.replace('Порядок выполнения работы', escaped_table + 'Порядок выполнения работы')
            elif 'Содержание отчета' in content:
                content = content.replace('Содержание отчета', escaped_table + 'Содержание отчета')
            else:
                content = content + escaped_table
            return match.group(1) + content + match.group(3)
        
        chapters_ts = re.sub(pattern, replace_table, chapters_ts, flags=re.DOTALL)
        print(f"  ✓ {table_key} обновлена")
    
    print("\nСохранение...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(chapters_ts)
    print("Готово!")

if __name__ == "__main__":
    main()

