#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой скрипт для выделения важного текста жирным шрифтом в markdown файлах
"""

import re
from pathlib import Path

def is_already_bold(text, pos):
    """Проверяет, находится ли позиция внутри жирного текста"""
    # Проверяем, есть ли ** перед позицией (нечетное количество)
    before = text[:pos]
    count = before.count('**')
    return count % 2 == 1

def highlight_important_content(text):
    """Выделяет важные элементы в тексте"""
    
    # 1. Выделяем определения (паттерн: "Термин – это определение")
    text = re.sub(
        r'([А-ЯЁ][А-Яа-яё\s]{3,50}?)\s*–\s*это\s+([^\.\n]+)',
        lambda m: f'**{m.group(1).strip()}** – это {m.group(2)}',
        text
    )
    
    # 2. Выделяем названия моделей (проверяем, что не выделены)
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
        # Простая замена, если еще не выделено
        pattern = f'({model})'
        def replace_func(m):
            match_text = m.group(1)
            start = m.start()
            # Проверяем, не выделено ли уже
            if '**' + match_text + '**' not in text[max(0, start-10):start+len(match_text)+10]:
                return f'**{match_text}**'
            return match_text
        text = re.sub(pattern, replace_func, text, flags=re.IGNORECASE)
    
    # 3. Выделяем важные проценты
    text = re.sub(r'\b(75%|более\s+75%)\b', r'**\1**', text)
    
    # 4. Выделяем термины в кавычках
    quoted_terms = [
        r'«чёрный ящик»',
        r'«серый ящик»',
        r'«белый ящик»',
        r'«просвечивающий ящик»'
    ]
    for term in quoted_terms:
        if f'**{term}**' not in text:
            text = re.sub(term, f'**{term}**', text, flags=re.IGNORECASE)
    
    # 5. Выделяем принципы
    text = re.sub(
        r'(принцип информационной закрытости)',
        r'**\1**',
        text,
        flags=re.IGNORECASE
    )
    
    # 6. Выделяем важные характеристики
    metrics = [
        r'сила связности',
        r'коэффициент объединения',
        r'коэффициент разветвления',
    ]
    for metric in metrics:
        if f'**{metric}**' not in text:
            text = re.sub(
                f'({metric})',
                r'**\1**',
                text,
                flags=re.IGNORECASE
            )
    
    # 7. Выделяем важные утверждения
    important_phrases = [
        r'Справедлива следующая аксиома[^:]*:',
        r'Важность проектирования[^:]*:',
        r'Следует отметить[^,]+,',
    ]
    for phrase in important_phrases:
        if f'**{phrase}**' not in text:
            text = re.sub(
                f'({phrase})',
                r'**\1**',
                text,
                flags=re.IGNORECASE
            )
    
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

