#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для извлечения текста из PDF файла
Требуется установка: pip install PyPDF2 или pip install pdfplumber
"""

import sys
import os

def extract_with_pypdf2(pdf_path):
    """Извлечение текста с помощью PyPDF2"""
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"Ошибка при извлечении текста: {e}")
        return None

def extract_with_pdfplumber(pdf_path):
    """Извлечение текста с помощью pdfplumber (более точное)"""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"Ошибка при извлечении текста: {e}")
        return None

def main():
    # Поиск PDF файла
    pdf_files = []
    current_dir = os.getcwd()
    
    # Ищем в текущей директории
    for file in os.listdir(current_dir):
        if file.lower().endswith('.pdf') and 'litovka' in file.lower():
            pdf_files.append(os.path.join(current_dir, file))
    
    # Если не найден, проверяем аргументы командной строки
    if len(sys.argv) > 1:
        pdf_files.append(sys.argv[1])
    
    if not pdf_files:
        print("PDF файл не найден!")
        print("Использование: python extract_pdf.py [путь_к_файлу.pdf]")
        print("\nИли поместите файл litovka (2).pdf в текущую директорию")
        return
    
    pdf_path = pdf_files[0]
    print(f"Обработка файла: {pdf_path}")
    
    # Пробуем извлечь текст
    text = None
    
    # Сначала пробуем pdfplumber (более точный)
    text = extract_with_pdfplumber(pdf_path)
    
    # Если не получилось, пробуем PyPDF2
    if not text:
        text = extract_with_pypdf2(pdf_path)
    
    if not text:
        print("\nОшибка: Не удалось извлечь текст.")
        print("Установите одну из библиотек:")
        print("  pip install pdfplumber")
        print("  или")
        print("  pip install PyPDF2")
        return
    
    # Сохраняем в файл
    output_file = "extracted_text.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"\nТекст успешно извлечен и сохранен в {output_file}")
    print(f"Всего символов: {len(text)}")
    print(f"Всего строк: {len(text.splitlines())}")

if __name__ == "__main__":
    main()

