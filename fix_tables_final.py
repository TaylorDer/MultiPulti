#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальное исправление таблиц с правильным парсингом многострочных заголовков
"""

import re

def parse_table_headers_smart(lines, start_idx):
    """Умный парсинг многострочных заголовков"""
    i = start_idx
    
    # Пропускаем "Таблица X.Y"
    if i < len(lines) and re.match(r'^Таблица', lines[i], re.IGNORECASE):
        i += 1
    
    # Пропускаем пустые строки
    while i < len(lines) and not lines[i].strip():
        i += 1
    
    # Собираем все строки заголовков (до первой строки с данными)
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
    
    # Парсим заголовки
    headers = []
    
    if len(header_lines) >= 2:
        # Объединяем первые строки для "№ варианта"
        first_part = ' '.join([h for h in header_lines[:2] if h]).strip()
        if 'варианта' in first_part or first_part == '№':
            headers.append('№ варианта')
        else:
            headers.append(first_part if first_part else '№ варианта')
        
        # Остальные строки - это заголовки колонок
        if len(header_lines) >= 3:
            # Берем строку с основными заголовками (обычно предпоследняя)
            main_header = header_lines[-2] if len(header_lines) >= 3 else header_lines[-1]
            # И строку с подзаголовками (последняя)
            sub_header = header_lines[-1] if len(header_lines) >= 2 else ""
            
            # Разбиваем на колонки
            # Ищем паттерны типа "С , %", "m, кг/с", "Т, °С"
            # Разбиваем по пробелам, но учитываем, что некоторые части могут быть объединены
            
            # Простой подход: разбиваем по пробелам и группируем
            main_parts = main_header.split()
            sub_parts = sub_header.split() if sub_header else []
            
            # Объединяем части заголовков
            col_idx = 0
            while col_idx < len(main_parts):
                col_name = main_parts[col_idx]
                # Если следующая часть - это единица измерения или продолжение
                if col_idx + 1 < len(main_parts) and main_parts[col_idx + 1] in [',', '%', '°С', 'кг/с', 'кг/c']:
                    col_name += ' ' + main_parts[col_idx + 1]
                    col_idx += 1
                # Добавляем подзаголовок если есть
                if col_idx < len(sub_parts):
                    col_name += ' ' + sub_parts[col_idx]
                headers.append(col_name)
                col_idx += 1
    
    # Если не удалось распарсить, используем упрощенный вариант
    if len(headers) < 2:
        headers = ['№ варианта']
        # Пытаемся извлечь хотя бы количество колонок из первой строки данных
        if i < len(lines) and re.match(r'^\d+', lines[i]):
            first_data = lines[i].split()
            num_cols = len(first_data)
            headers.extend([f'Колонка {j+1}' for j in range(num_cols - 1)])
    
    return headers, i

def main():
    print("Чтение extracted_text_full.txt...")
    with open('extracted_text_full.txt', 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    lines = full_text.split('\n')
    
    # Тестируем на таблице 1.1
    print("Тестирование парсинга таблицы 1.1...")
    for i, line in enumerate(lines):
        if 'Таблица 1.1' in line:
            headers, data_start = parse_table_headers_smart(lines, i)
            print(f"Заголовки: {headers}")
            print(f"Первая строка данных: {lines[data_start] if data_start < len(lines) else 'N/A'}")
            break

if __name__ == "__main__":
    main()

