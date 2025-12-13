#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для выделения важных терминов и фраз жирным шрифтом в markdown файлах
"""

import re
from pathlib import Path

# Список важных терминов и фраз для выделения жирным
IMPORTANT_TERMS = [
    # Основные процессы
    r'\b(анализ|синтез|сопровождение)\b',
    r'\b(проектирование|кодирование|тестирование)\b',
    r'\b(разработка данных|разработка архитектуры|процедурная разработка)\b',
    
    # Модели
    r'\b(информационная модель|функциональная модель|поведенческая модель)\b',
    r'\b(модель хранилища данных|модель клиент-сервер|трёхуровневая модель|модель абстрактной машины)\b',
    r'\b(модель централизованного управления|модель событийного управления|модель вызов-возврат|модель менеджера)\b',
    r'\b(широковещательная модель|модель, управляемая прерываниями)\b',
    r'\b(модель потока данных|модель объектов)\b',
    
    # Основные понятия
    r'\b(модуль|модульность|информационная закрытость)\b',
    r'\b(связность|сцепление)\b',
    r'\b(функциональная связность|информационная связность|коммуникативная связность)\b',
    r'\b(процедурная связность|временная связность|логическая связность|связность по совпадению)\b',
    r'\b(сцепление по данным|сцепление по образцу|сцепление по управлению)\b',
    r'\b(сцепление по внешним ссылкам|сцепление по общей области|сцепление по содержанию)\b',
    
    # Объектно-ориентированные понятия
    r'\b(абстрагирование|абстракция|инкапсуляция)\b',
    r'\b(объект|класс|наследование|полиморфизм)\b',
    r'\b(агрегация|зависимость|ассоциация|конкретизация)\b',
    r'\b(алгоритмическая декомпозиция|объектно-ориентированная декомпозиция)\b',
    
    # UML
    r'\b(UML|Unified Modeling Language)\b',
    r'\b(диаграмма классов|диаграмма объектов|диаграмма Use Case)\b',
    r'\b(диаграмма последовательности|диаграмма сотрудничества|диаграмма схем состояний)\b',
    r'\b(диаграмма деятельности|компонентная диаграмма|диаграмма размещения)\b',
    
    # Процессы разработки
    r'\b(классический жизненный цикл|макетирование|инкрементная модель)\b',
    r'\b(быстрая разработка приложений|RAD|спиральная модель)\b',
    r'\b(компонентно-ориентированная модель|тяжеловесные процессы|облегчённые процессы)\b',
    r'\b(ХР-процесс|экстремальное программирование|XP)\b',
    
    # Важные утверждения
    r'\b(качество|сложность|иерархическая структура)\b',
    r'\b(чёрный ящик|белый ящик|серый ящик)\b',
    
    # Технологии
    r'\b(ТКПО|CASE-системы|CASE)\b',
    r'\b(ПС|ПО|БД|СУБД|GUI)\b',
]

def format_text_with_bold(text):
    """Выделяет важные термины жирным шрифтом"""
    result = text
    
    # Применяем паттерны для выделения терминов
    for pattern in IMPORTANT_TERMS:
        # Ищем все вхождения, но не те, которые уже в жирном формате
        matches = list(re.finditer(pattern, result, re.IGNORECASE))
        # Обрабатываем с конца, чтобы не сбить индексы
        for match in reversed(matches):
            start, end = match.span()
            # Проверяем, не находится ли уже в жирном формате
            before = result[max(0, start-2):start]
            after = result[end:min(len(result), end+2)]
            if '**' not in before and '**' not in after:
                # Выделяем жирным
                matched_text = result[start:end]
                result = result[:start] + '**' + matched_text + '**' + result[end:]
    
    # Выделяем определения (фразы типа "X – это Y" или "X определяется как Y")
    # Более точные паттерны для определений
    definition_patterns = [
        r'([А-Я][А-Яа-я\s]{4,25}?)\s*–\s*(это|определяется|является|представляет)',
    ]
    
    for pattern in definition_patterns:
        matches = list(re.finditer(pattern, result, re.IGNORECASE))
        for match in reversed(matches):
            start, end = match.span(1)  # Первая группа - термин
            # Проверяем, что это не слишком короткое слово и не часть другого выделения
            matched_text = result[start:end].strip()
            if len(matched_text) < 5 or len(matched_text) > 30:
                continue
            before = result[max(0, start-2):start]
            after = result[end:min(len(result), end+2)]
            if '**' not in before and '**' not in after and matched_text.lower() not in ['по', 'на', 'в', 'с', 'к', 'от']:
                result = result[:start] + '**' + matched_text + '**' + result[end:]
    
    # Выделяем важные числа и проценты
    result = re.sub(r'(\d+%|\d+\s*процентов)', r'**\1**', result)
    result = re.sub(r'более\s+(\d+%|\d+\s*процентов)', r'более **\1**', result)
    
    # Выделяем аксиомы и важные утверждения
    axiom_patterns = [
        r'(Справедлива\s+следующая\s+аксиома[^:]*:)',
        r'(Важно\s+отметить[^:]*:)',
        r'(Следует\s+отметить[^:]*:)',
    ]
    
    for pattern in axiom_patterns:
        matches = list(re.finditer(pattern, result, re.IGNORECASE))
        for match in reversed(matches):
            start, end = match.span()
            before = result[max(0, start-2):start]
            after = result[end:min(len(result), end+2)]
            if '**' not in before and '**' not in after:
                matched_text = result[start:end]
                result = result[:start] + '**' + matched_text + '**' + result[end:]
    
    # Выделяем важные модели и подходы, которые могли быть пропущены
    additional_terms = [
        r'\b(функциональная модель)\b',
        r'\b(поведенческая модель)\b',
        r'\b(информационная модель анализа)\b',
        r'\b(предварительное проектирование)\b',
        r'\b(детальное проектирование)\b',
        r'\b(интерфейсное проектирование)\b',
    ]
    
    for pattern in additional_terms:
        matches = list(re.finditer(pattern, result, re.IGNORECASE))
        for match in reversed(matches):
            start, end = match.span()
            before = result[max(0, start-2):start]
            after = result[end:min(len(result), end+2)]
            if '**' not in before and '**' not in after:
                matched_text = result[start:end]
                result = result[:start] + '**' + matched_text + '**' + result[end:]
    
    # Убираем двойное выделение
    result = re.sub(r'\*\*\*\*([^*]+)\*\*\*\*', r'**\1**', result)
    # Убираем выделение коротких слов-предлогов
    result = re.sub(r'\*\*(по|на|в|с|к|от|за|под|над|при|про|без|для|из|от|до|у|о|об|со|во)\*\*', r'\1', result, flags=re.IGNORECASE)
    
    return result

def process_markdown_file(filepath):
    """Обрабатывает один markdown файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Сохраняем заголовок
        lines = content.split('\n')
        if lines and lines[0].startswith('#'):
            header = lines[0] + '\n'
            if len(lines) > 1 and lines[1].strip() == '':
                header += '\n'
            body_start = 1 if lines[1].strip() == '' else 1
            body = '\n'.join(lines[body_start:])
        else:
            header = ''
            body = content
        
        # Форматируем тело текста
        formatted_body = format_text_with_bold(body)
        
        # Объединяем
        formatted_content = header + formatted_body
        
        # Сохраняем
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        return True
    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}")
        return False

def main():
    chapters_dir = Path('public/content/chapters')
    
    if not chapters_dir.exists():
        print(f"Директория {chapters_dir} не найдена!")
        return
    
    markdown_files = list(chapters_dir.glob('*.md'))
    print(f"Найдено {len(markdown_files)} markdown файлов")
    
    processed = 0
    for md_file in markdown_files:
        if process_markdown_file(md_file):
            processed += 1
            print(f"Обработан: {md_file.name}")
    
    print(f"\nОбработано файлов: {processed}/{len(markdown_files)}")
    
    # Также обрабатываем файлы в src/content/chapters
    src_chapters_dir = Path('src/content/chapters')
    if src_chapters_dir.exists():
        src_markdown_files = list(src_chapters_dir.glob('*.md'))
        print(f"\nОбработка файлов в {src_chapters_dir}...")
        for md_file in src_markdown_files:
            if process_markdown_file(md_file):
                processed += 1
        print(f"Всего обработано: {processed} файлов")

if __name__ == '__main__':
    main()

