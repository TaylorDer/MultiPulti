#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Преобразование таблиц в формат Markdown
"""

import re

def convert_table_to_markdown(text):
    """Преобразует таблицы в формат Markdown"""
    lines = text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Ищем начало таблицы
        if re.match(r'^Таблица \d+\.\d+', line, re.IGNORECASE):
            result.append(f'\n## {line}\n')
            i += 1
            
            # Пропускаем пустые строки
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            # Собираем заголовки
            headers = []
            header_lines = []
            
            # Читаем заголовки (обычно 2-3 строки)
            while i < len(lines) and lines[i].strip() and not re.match(r'^\d+', lines[i].strip()):
                header_line = lines[i].strip()
                if header_line and not re.match(r'^Продолжение', header_line, re.IGNORECASE):
                    header_lines.append(header_line)
                i += 1
            
            # Объединяем заголовки
            if header_lines:
                # Разбиваем на колонки (приблизительно)
                header_text = ' '.join(header_lines)
                # Простое разбиение по пробелам (можно улучшить)
                headers = [h for h in header_text.split() if h and h != '№']
                if headers:
                    # Добавляем номер варианта в начало
                    headers = ['№ варианта'] + headers
            
            # Если не удалось распарсить заголовки, используем простой вариант
            if not headers:
                headers = ['№ варианта', 'Параметры']
            
            # Создаем Markdown таблицу
            result.append('| ' + ' | '.join(headers) + ' |')
            result.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
            
            # Читаем данные
            while i < len(lines):
                line = lines[i].strip()
                
                # Проверяем, не началась ли новая таблица или секция
                if re.match(r'^Продолжение табл\.', line, re.IGNORECASE):
                    i += 1
                    # Пропускаем пустые строки и заголовки продолжения
                    while i < len(lines) and (not lines[i].strip() or not re.match(r'^\d+', lines[i].strip())):
                        if re.match(r'^№', lines[i].strip()):
                            i += 1
                        else:
                            i += 1
                    continue
                
                if re.match(r'^(Лабораторная|Практическая|КУРСОВАЯ|СПИСОК)', line, re.IGNORECASE):
                    break
                
                # Парсим строку данных
                if re.match(r'^\d+', line):
                    # Разбиваем на колонки
                    parts = line.split()
                    if len(parts) > 1:
                        # Формируем строку таблицы
                        row = '| ' + ' | '.join(parts) + ' |'
                        result.append(row)
                
                i += 1
            
            result.append('')  # Пустая строка после таблицы
            continue
        
        result.append(lines[i])
        i += 1
    
    return '\n'.join(result)

def main():
    print("Чтение chapters.ts...")
    with open('src/data/chapters.ts', 'r', encoding='utf-8') as f:
        chapters_ts = f.read()
    
    # Находим все content блоки и преобразуем таблицы
    pattern = r"(content: `)(.*?)(`[,\)])"
    
    def convert_content(match):
        content = match.group(2)
        # Распаковываем
        content = content.replace('\\n', '\n')
        # Преобразуем таблицы
        content = convert_table_to_markdown(content)
        # Упаковываем обратно
        content = content.replace('\n', '\\n')
        content = content.replace('`', '\\`')
        content = content.replace('${', '\\${')
        return match.group(1) + content + match.group(3)
    
    new_chapters_ts = re.sub(pattern, convert_content, chapters_ts, flags=re.DOTALL)
    
    print("Сохранение...")
    with open('src/data/chapters.ts', 'w', encoding='utf-8') as f:
        f.write(new_chapters_ts)
    
    print("Готово! Таблицы преобразованы в Markdown формат.")

if __name__ == "__main__":
    main()

