#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для выделения важного текста жирным шрифтом в markdown файлах
"""

import re
import os
from pathlib import Path

def highlight_important_content(text):
    """Выделяет важные элементы в тексте"""
    
    # 1. Выделяем определения (паттерн: "Термин – это определение")
    text = re.sub(
        r'([А-ЯЁ][А-Яа-яё\s]{3,40}?)\s*–\s*это\s+([^\.\n]+)',
        lambda m: f'**{m.group(1).strip()}** – это {m.group(2)}',
        text
    )
    
    # 2. Выделяем названия моделей (если еще не выделены)
    models = [
        (r'(?<!\*\*)(модель хранилища данных)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель клиент-сервер)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(трёхуровневая модель)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель абстрактной машины)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель вызов-возврат)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель менеджера)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(широковещательная модель)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель.*управляемая прерываниями)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель потока данных)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель объектов)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(классический жизненный цикл)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(инкрементная модель)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель быстрой разработки приложений)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(спиральная модель)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(компонентно-ориентированная модель)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(ХР-процесс)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(модель СММ)(?!\*\*)', r'**\1**'),
    ]
    
    for pattern, replacement in models:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # 3. Выделяем типы связности и сцепления с их значениями
    text = re.sub(
        r'(?<!\*\*)([А-ЯЁ][а-яё]+\s+связность)\s*\([А-ЯЁ]{2,}\s*=\s*[0-9]+\)(?!\*\*)',
        r'**\1**',
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(?<!\*\*)([А-ЯЁ][а-яё]+\s+сцепление)\s*\([А-ЯЁ]{2,}\s*=\s*[0-9]+\)(?!\*\*)',
        r'**\1**',
        text,
        flags=re.IGNORECASE
    )
    
    # 4. Выделяем важные проценты и числа
    text = re.sub(r'\b(75%|более\s+75%)\b', r'**\1**', text)
    
    # 5. Выделяем термины в кавычках типа «чёрный ящик»
    quoted_terms = [
        r'«чёрный ящик»',
        r'«серый ящик»',
        r'«белый ящик»',
        r'«просвечивающий ящик»'
    ]
    for term in quoted_terms:
        if f'**{term}**' not in text:
            text = re.sub(term, f'**{term}**', text, flags=re.IGNORECASE)
    
    # 6. Выделяем принципы (используем raw strings для избежания предупреждений)
    principles = [
        (r'(?<!\*\*)(принцип информационной закрытости)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(принцип.*модульности)(?!\*\*)', r'**\1**'),
    ]
    for pattern, replacement in principles:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # 7. Выделяем важные характеристики и метрики
    metrics = [
        (r'(?<!\*\*)(сила связности)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(коэффициент объединения)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(коэффициент разветвления)(?!\*\*)', r'**\1**'),
    ]
    for pattern, replacement in metrics:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # 8. Выделяем важные утверждения
    important_phrases = [
        (r'(?<!\*\*)(Справедлива следующая аксиома[^:]*:)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(Важность проектирования[^:]*:)(?!\*\*)', r'**\1**'),
        (r'(?<!\*\*)(Следует отметить[^,]+,)(?!\*\*)', r'**\1**'),
    ]
    for pattern, replacement in important_phrases:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # 9. Выделяем ключевые процессы и этапы в важных контекстах
    # "три процесса – анализ, синтез и сопровождение"
    text = re.sub(
        r'(три\s+процесса\s*–\s*)(анализ)(,\s*)(синтез)(\s+и\s+)(сопровождение)',
        r'\1**\2**\3**\4**\5**\6**',
        text,
        flags=re.IGNORECASE
    )
    
    # "три этапа синтеза: проектирование ПС, кодирование ПС, тестирование ПС"
    text = re.sub(
        r'(три\s+этапа[^:]*:\s*)(проектирование\s+ПС)(,\s*)(кодирование\s+ПС)(,\s*)(тестирование\s+ПС)',
        r'\1**\2**\3**\4**\5**\6**',
        text,
        flags=re.IGNORECASE
    )
    
    # 10. Выделяем важные термины в начале предложений
    key_terms_at_start = [
        r'(^|\n|\.\s+)(Модульность)(\s+–\s+)',
        r'(^|\n|\.\s+)(Связность)(\s+–\s+)',
        r'(^|\n|\.\s+)(Сцепление)(\s+–\s+)',
        r'(^|\n|\.\s+)(Проектирование)(\s+–\s+)',
        r'(^|\n|\.\s+)(Инкапсуляция)(\s+–\s+)',
        r'(^|\n|\.\s+)(Абстракция)(\s+–\s+)',
        r'(^|\n|\.\s+)(Наследование)(\s+–\s+)',
        r'(^|\n|\.\s+)(Полиморфизм)(\s+–\s+)',
    ]
    
    for pattern in key_terms_at_start:
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
            print(f"Директория {chapters_dir} не найдена, пропускаем")
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
