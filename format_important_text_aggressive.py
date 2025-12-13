#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Агрессивный скрипт для выделения важного текста жирным шрифтом в markdown файлах
"""

import re
from pathlib import Path

def highlight_important_content(text):
    """Выделяет важные элементы в тексте"""
    
    # 1. Выделяем все определения (паттерн: "Термин – это определение")
    text = re.sub(
        r'([А-ЯЁ][А-Яа-яё\s]{3,50}?)\s*–\s*это\s+([^\.\n]+)',
        lambda m: f'**{m.group(1).strip()}** – это {m.group(2)}',
        text
    )
    
    # 2. Выделяем термины после "– это результат", "– это мера" и т.д.
    text = re.sub(
        r'([А-ЯЁ][А-Яа-яё\s]{3,50}?)\s*–\s*(это\s+)?(результат|мера|характеристика|свойство|принцип|этап|процесс|набор|описание)',
        lambda m: f'**{m.group(1).strip()}** – {m.group(2) or ""}{m.group(3)}',
        text
    )
    
    # 3. Выделяем названия моделей
    models = [
        r'модель хранилища данных',
        r'модель клиент-сервер',
        r'трёхуровневая модель',
        r'модель абстрактной машины',
        r'модель вызов-возврат',
        r'модель менеджера',
        r'широковещательная модель',
        r'модель.*управляемая прерываниями',
        r'модель потока данных',
        r'модель объектов',
        r'классический жизненный цикл',
        r'инкрементная модель',
        r'модель быстрой разработки приложений',
        r'спиральная модель',
        r'компонентно-ориентированная модель',
        r'ХР-процесс',
        r'модель СММ'
    ]
    
    for model in models:
        # Выделяем, если еще не выделено
        pattern = f'(?<!\\*\\*)({model})(?!\\*\\*)'
        text = re.sub(pattern, r'**\1**', text, flags=re.IGNORECASE)
    
    # 4. Выделяем ключевые термины (если еще не выделены)
    key_terms = [
        r'\bмодуль\b',
        r'\bмодульность\b',
        r'\bсвязность\b',
        r'\bсцепление\b',
        r'\bпроектирование\b',
        r'\bкодирование\b',
        r'\bтестирование\b',
        r'\bанализ\b',
        r'\bсинтез\b',
        r'\bсопровождение\b',
        r'\bобъект\b',
        r'\bкласс\b',
        r'\bинкапсуляция\b',
        r'\bабстракция\b',
        r'\bнаследование\b',
        r'\bполиморфизм\b',
        r'\bагрегация\b',
        r'\bинтерфейс\b',
        r'\bкомпонент\b',
        r'\bкооперация\b',
        r'\bинформационная закрытость\b',
        r'\bинформационная модель\b',
        r'\bфункциональная модель\b',
        r'\bповеденческая модель\b',
        r'\bразработка данных\b',
        r'\bразработка архитектуры\b',
        r'\bпроцедурная разработка\b',
    ]
    
    for term in key_terms:
        # Выделяем только если еще не выделено и это отдельное слово
        pattern = f'(?<!\\*\\*)(?<!\\*)({term})(?!\\*\\*)(?!\\*)'
        text = re.sub(pattern, r'**\1**', text, flags=re.IGNORECASE)
    
    # 5. Выделяем типы связности и сцепления
    text = re.sub(
        r'(?<!\\*\\*)([А-ЯЁ][а-яё]+\s+связность)\s*\([А-ЯЁ]{2,}\s*=\s*[0-9]+\)(?!\\*\\*)',
        r'**\1**',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(?<!\\*\\*)([А-ЯЁ][а-яё]+\s+сцепление)\s*\([А-ЯЁ]{2,}\s*=\s*[0-9]+\)(?!\\*\\*)',
        r'**\1**',
        text,
        flags=re.IGNORECASE
    )
    
    # 6. Выделяем важные проценты
    text = re.sub(r'\b(75%|более\s+75%)\b', r'**\1**', text)
    
    # 7. Выделяем термины в кавычках
    quoted_terms = [
        r'«чёрный ящик»',
        r'«серый ящик»',
        r'«белый ящик»',
        r'«просвечивающий ящик»'
    ]
    for term in quoted_terms:
        if f'**{term}**' not in text:
            text = re.sub(term, f'**{term}**', text, flags=re.IGNORECASE)
    
    # 8. Выделяем принципы
    text = re.sub(
        r'(?<!\\*\\*)(принцип информационной закрытости)(?!\\*\\*)',
        r'**\1**',
        text,
        flags=re.IGNORECASE
    )
    
    # 9. Выделяем важные характеристики
    metrics = [
        r'сила связности',
        r'коэффициент объединения',
        r'коэффициент разветвления',
    ]
    for metric in metrics:
        text = re.sub(
            f'(?<!\\*\\*)({metric})(?!\\*\\*)',
            r'**\1**',
            text,
            flags=re.IGNORECASE
        )
    
    # 10. Выделяем важные утверждения
    important_phrases = [
        r'Справедлива следующая аксиома',
        r'Важность проектирования',
        r'Следует отметить',
    ]
    for phrase in important_phrases:
        text = re.sub(
            f'(?<!\\*\\*)({phrase}[^:]*:)(?!\\*\\*)',
            r'**\1**',
            text,
            flags=re.IGNORECASE
        )
    
    # 11. Выделяем процессы в списках
    text = re.sub(
        r'(три\s+процесса\s*–\s*)(анализ)(,\s*)(синтез)(\s+и\s+)(сопровождение)',
        r'\1**\2**\3**\4**\5**\6**',
        text,
        flags=re.IGNORECASE
    )
    
    text = re.sub(
        r'(три\s+этапа[^:]*:\s*)(проектирование\s+ПС)(,\s*)(кодирование\s+ПС)(,\s*)(тестирование\s+ПС)',
        r'\1**\2**\3**\4**\5**\6**',
        text,
        flags=re.IGNORECASE
    )
    
    # 12. Выделяем важные слова в начале предложений
    important_start_words = [
        r'(^|\n|\.\s+)(Модульность)(\s+–\s+)',
        r'(^|\n|\.\s+)(Связность)(\s+–\s+)',
        r'(^|\n|\.\s+)(Сцепление)(\s+–\s+)',
        r'(^|\n|\.\s+)(Проектирование)(\s+–\s+)',
        r'(^|\n|\.\s+)(Инкапсуляция)(\s+–\s+)',
        r'(^|\n|\.\s+)(Абстракция)(\s+–\s+)',
        r'(^|\n|\.\s+)(Наследование)(\s+–\s+)',
        r'(^|\n|\.\s+)(Полиморфизм)(\s+–\s+)',
    ]
    
    for pattern in important_start_words:
        text = re.sub(pattern, r'\1**\2**\3', text, flags=re.MULTILINE)
    
    return text

def process_markdown_file(filepath):
    """Обрабатывает один markdown файл"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Применяем форматирование
        content = highlight_important_content(content)
        
        # Записываем обратно только если были изменения
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}")
        return False

def main():
    chapters_dirs = [
        Path('public/content/chapters'),
        Path('src/content/chapters')
    ]
    
    total_changed = 0
    
    for chapters_dir in chapters_dirs:
        if not chapters_dir.exists():
            continue
        
        files = list(chapters_dir.glob('*.md'))
        print(f"\nОбрабатываю {len(files)} файлов в {chapters_dir}")
        
        for filepath in files:
            if process_markdown_file(filepath):
                total_changed += 1
                print(f"  ✓ {filepath.name}")
    
    print(f"\nВсего обработано файлов: {total_changed}")
    print("Готово!")

if __name__ == '__main__':
    main()

