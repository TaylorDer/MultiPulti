#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полное извлечение текста и изображений из PDF
"""

import sys
import os

def extract_with_pdfplumber(pdf_path):
    """Извлечение текста и изображений с помощью pdfplumber"""
    try:
        import pdfplumber
        import fitz  # PyMuPDF для изображений
        
        text_content = []
        images_info = []
        
        # Извлекаем текст
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(f"=== Страница {page_num} ===\n{text}\n")
        
        # Извлекаем изображения
        pdf_doc = fitz.open(pdf_path)
        for page_num in range(len(pdf_doc)):
            page = pdf_doc[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Сохраняем изображение
                image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                image_path = f"public/images/{image_filename}"
                
                os.makedirs("public/images", exist_ok=True)
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                images_info.append({
                    'page': page_num + 1,
                    'filename': image_filename,
                    'path': f"/images/{image_filename}"
                })
        
        pdf_doc.close()
        
        return '\n'.join(text_content), images_info
        
    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Установите: pip install pdfplumber PyMuPDF")
        return None, None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None

def main():
    pdf_path = "litovka (2).pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Файл {pdf_path} не найден!")
        return
    
    print("Извлечение текста и изображений...")
    text, images = extract_with_pdfplumber(pdf_path)
    
    if text:
        with open('extracted_text_full.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Текст сохранен в extracted_text_full.txt ({len(text)} символов)")
    
    if images:
        print(f"Извлечено изображений: {len(images)}")
        with open('extracted_images.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(images, f, ensure_ascii=False, indent=2)
        print("Информация об изображениях сохранена в extracted_images.json")
    
    print("Готово!")

if __name__ == "__main__":
    main()

