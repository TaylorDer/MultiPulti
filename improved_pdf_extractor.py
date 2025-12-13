"""
Улучшенный скрипт для извлечения данных из PDF
Использует более продвинутые методы для распознавания формул, таблиц и структуры
"""

import fitz  # PyMuPDF
import pdfplumber
import re
from pathlib import Path
import json

def extract_with_pdfplumber(pdf_path):
    """Извлечение текста и таблиц с помощью pdfplumber"""
    print("📄 Извлечение с помощью pdfplumber...")
    
    text_content = []
    tables_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"  Обработка страницы {page_num}...")
            
            # Извлечение текста
            text = page.extract_text()
            if text:
                text_content.append({
                    'page': page_num,
                    'text': text
                })
            
            # Извлечение таблиц
            tables = page.extract_tables()
            if tables:
                for table_num, table in enumerate(tables, 1):
                    tables_data.append({
                        'page': page_num,
                        'table_num': table_num,
                        'table': table
                    })
    
    return text_content, tables_data

def extract_with_pymupdf(pdf_path):
    """Извлечение с помощью PyMuPDF (лучше для изображений и структуры)"""
    print("📄 Извлечение с помощью PyMuPDF...")
    
    doc = fitz.open(pdf_path)
    pages_data = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"  Обработка страницы {page_num + 1}...")
        
        # Извлечение текста с сохранением координат
        blocks = page.get_text("dict")
        
        # Извлечение изображений
        images = []
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            images.append({
                'index': img_index,
                'xref': xref,
                'ext': image_ext,
                'size': len(image_bytes)
            })
        
        pages_data.append({
            'page': page_num + 1,
            'blocks': blocks,
            'images': images,
            'text': page.get_text()
        })
    
    doc.close()
    return pages_data

def analyze_formulas(text):
    """Попытка найти формулы в тексте"""
    formulas = []
    
    # Паттерны для поиска формул
    patterns = [
        r'\\tag\{[^}]+\}',  # \tag{1.42}
        r'[a-zA-Z_а-яА-Я]+\s*=\s*[^;]+;',  # уравнения вида m = ...
        r'[a-zA-Z_а-яА-Я]+\s*\([^)]+\)\s*=',  # функции вида f(x) =
        r'\\[a-zA-Z]+\{[^}]+\}',  # LaTeX команды
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            formulas.append({
                'formula': match.group(),
                'position': match.start(),
                'pattern': pattern
            })
    
    return formulas

def format_table_as_markdown(table):
    """Форматирование таблицы в Markdown"""
    if not table or len(table) == 0:
        return ""
    
    # Определяем количество столбцов
    max_cols = max(len(row) for row in table if row)
    
    # Нормализуем строки (добавляем пустые ячейки если нужно)
    normalized_table = []
    for row in table:
        if row:
            normalized_row = row + [''] * (max_cols - len(row))
            normalized_table.append(normalized_row[:max_cols])
    
    if len(normalized_table) == 0:
        return ""
    
    # Создаем Markdown таблицу
    markdown_lines = []
    
    # Заголовок (первая строка)
    if normalized_table:
        header = normalized_table[0]
        markdown_lines.append('| ' + ' | '.join(str(cell) if cell else '' for cell in header) + ' |')
        markdown_lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
        
        # Данные
        for row in normalized_table[1:]:
            markdown_lines.append('| ' + ' | '.join(str(cell) if cell else '' for cell in row) + ' |')
    
    return '\n'.join(markdown_lines)

def main():
    pdf_path = Path("litovka (2).pdf")
    
    if not pdf_path.exists():
        print(f"❌ Файл {pdf_path} не найден!")
        return
    
    print(f"📖 Обработка PDF: {pdf_path}")
    print("=" * 60)
    
    # Метод 1: pdfplumber (лучше для таблиц)
    print("\n1️⃣ Метод 1: pdfplumber")
    text_content, tables_data = extract_with_pdfplumber(pdf_path)
    
    print(f"   ✓ Извлечено страниц с текстом: {len(text_content)}")
    print(f"   ✓ Найдено таблиц: {len(tables_data)}")
    
    # Метод 2: PyMuPDF (лучше для структуры и изображений)
    print("\n2️⃣ Метод 2: PyMuPDF")
    pages_data = extract_with_pymupdf(pdf_path)
    
    print(f"   ✓ Обработано страниц: {len(pages_data)}")
    total_images = sum(len(page['images']) for page in pages_data)
    print(f"   ✓ Найдено изображений: {total_images}")
    
    # Анализ формул
    print("\n3️⃣ Поиск формул...")
    all_text = '\n'.join([page['text'] for page in text_content])
    formulas = analyze_formulas(all_text)
    print(f"   ✓ Найдено потенциальных формул: {len(formulas)}")
    
    # Сохранение результатов
    output_dir = Path("pdf_extraction_improved")
    output_dir.mkdir(exist_ok=True)
    
    # Сохраняем текст
    with open(output_dir / "extracted_text.txt", "w", encoding="utf-8") as f:
        for page_data in text_content:
            f.write(f"\n{'='*60}\n")
            f.write(f"СТРАНИЦА {page_data['page']}\n")
            f.write(f"{'='*60}\n\n")
            f.write(page_data['text'])
            f.write("\n\n")
    
    # Сохраняем таблицы
    with open(output_dir / "extracted_tables.md", "w", encoding="utf-8") as f:
        for table_data in tables_data:
            f.write(f"\n## Таблица на странице {table_data['page']}, таблица #{table_data['table_num']}\n\n")
            markdown_table = format_table_as_markdown(table_data['table'])
            f.write(markdown_table)
            f.write("\n\n")
    
    # Сохраняем формулы
    with open(output_dir / "extracted_formulas.txt", "w", encoding="utf-8") as f:
        for formula in formulas[:100]:  # Первые 100 формул
            f.write(f"{formula['formula']}\n")
    
    # Сохраняем метаданные
    metadata = {
        'total_pages': len(pages_data),
        'total_tables': len(tables_data),
        'total_formulas_found': len(formulas),
        'total_images': total_images
    }
    
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Результаты сохранены в папку: {output_dir}")
    print(f"\n📊 Статистика:")
    print(f"   - Страниц: {metadata['total_pages']}")
    print(f"   - Таблиц: {metadata['total_tables']}")
    print(f"   - Формул (найдено): {metadata['total_formulas_found']}")
    print(f"   - Изображений: {metadata['total_images']}")
    
    print("\n⚠️  ОГРАНИЧЕНИЯ:")
    print("   - Формулы могут быть не полностью распознаны")
    print("   - Таблицы могут требовать ручной правки")
    print("   - Для лучшего результата рекомендуется ручная обработка")

if __name__ == '__main__':
    try:
        main()
    except ImportError as e:
        print(f"❌ Ошибка: не установлена библиотека. Установите:")
        print(f"   pip install PyMuPDF pdfplumber")
        print(f"\nОшибка: {e}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

