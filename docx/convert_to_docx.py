#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re

def convert_markdown_to_docx(md_file, docx_file):
    """Конвертирует markdown файл в DOCX с правильным форматированием"""
    
    # Читаем markdown файл
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Создаем новый документ
    doc = Document()
    
    # Настройка шрифта по умолчанию
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    
    # Настройка полей (2 см со всех сторон)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.79)  # 2 см
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(0.79)
        section.right_margin = Inches(0.79)
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Пропускаем пустые строки
        if not line:
            i += 1
            continue
        
        # УДК
        if line.startswith('УДК'):
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            i += 1
            continue
        
        # Название статьи (заголовок)
        if line.startswith('РАЗРАБОТКА') or (line.isupper() and len(line) > 20 and not line.startswith('##')):
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(14)
            i += 1
            continue
        
        # Автор
        if line.startswith('Иванов И.О.') or (re.match(r'^[А-ЯЁ]+\s+[А-ЯЁ]\.[А-ЯЁ]\.', line)):
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue
        
        # Сведения об авторе
        if 'студент' in line.lower() or '@' in line:
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            i += 1
            continue
        
        # Заголовки разделов (##)
        if line.startswith('##'):
            text = line.replace('##', '').strip()
            p = doc.add_paragraph(text)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(14)
            i += 1
            continue
        
        # Подзаголовки (###)
        if line.startswith('###'):
            text = line.replace('###', '').strip()
            p = doc.add_paragraph(text)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(14)
            i += 1
            continue
        
        # Аннотация, Ключевые слова
        if line in ['Аннотация', 'Ключевые слова:', 'Введение', 'Материалы и методы', 
                   'Результаты', 'Обсуждение', 'Заключение', 'Список литературы']:
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.bold = True
            i += 1
            continue
        
        # Список литературы
        if re.match(r'^\d+\.\s', line):
            p = doc.add_paragraph(line)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            p.paragraph_format.left_indent = Inches(0.3)
            i += 1
            continue
        
        # Маркированные списки
        if line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # Удаляем markdown форматирование **текст**
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            p = doc.add_paragraph(text, style='List Bullet')
            i += 1
            continue
        
        # Обычный текст
        # Удаляем markdown форматирование
        text = line
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # **жирный**
        text = text.replace('(пустая строка)', '')
        
        if text.strip():
            p = doc.add_paragraph(text)
            # Красная строка для обычных абзацев
            if not line.startswith('##') and not re.match(r'^\d+\.\s', line):
                p.paragraph_format.first_line_indent = Inches(0.3)  # 0.75 см
        
        i += 1
    
    # Сохраняем документ
    doc.save(docx_file)
    print(f"Документ сохранен: {docx_file}")

if __name__ == '__main__':
    md_file = 'статья_кредитный_риск_ММПЕД_2025.md'
    docx_file = 'статья_кредитный_риск_ММПЕД_2025.docx'
    convert_markdown_to_docx(md_file, docx_file)

