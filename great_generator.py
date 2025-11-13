""""
Данный код использует config файл для структуры презентации
В папке с кодом должна находиться папка assets, в которой могут находитсятекстовые файлы и папки с изображениями.
При запуске генерируется pdf файл с презентацией.
"""

import os
import sys
from pathlib import Path

def get_base_dir():
    # Если запущено как exe через PyInstaller
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:  # Запуск как обычный .py
        return Path(__file__).parent

base_dir = get_base_dir()

# Парсинг конфиг файла
config_path = Path('config.txt')
if not config_path.is_file():
    with open('config.txt', 'w', encoding='utf-8') as config_file:
        config_file.write('# файл создан с нуля и требует заполнения\n')
        config_file.write('# t text_file\n')
        config_file.write('# i image_folder')
    print('Не был найден config файл. Создан новый. Требуется заполнение')
    


order = []
texts = {}
images = {}
with open('config.txt', 'r') as file:
    for line in file:
        tori, path, *_ = line.strip().split()
        order.append([tori, path])
        if tori == 't' and path not in texts.keys():
            texts[path] = []
            text_path = base_dir/'assets'/path
            if not text_path.is_file():
                print(f'Нет текстового файла {path}\nПроверьте файл config и папку assets')
                sys.exit(1)
            with open(text_path, 'r') as txt:
                for l in txt:
                    texts[path].append(l.strip())
        elif tori == 'i' and path not in images.keys():
            images[path] = []
            image_path = base_dir / 'assets' / path
            if not image_path.is_dir():
                print(f'Нет папки {path}\nПроверьте файл config и папку assets')
                sys.exit(1)
            for img in image_path.iterdir():
                if img.is_file():
                    images[path].append(img.name)

# Создание презентации
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random

#Размер страницы
PAGE_WIDTH, PAGE_HEIGHT = landscape((1920, 1020))
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans-Bold.ttf'))

c = canvas.Canvas("output.pdf", pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
font_size_base = 200
c.setFont('DejaVu', font_size_base)

def text_slide(path):
    random_text = random.choice(texts[path])
    texts[path].remove(random_text)

    max_width = PAGE_WIDTH * 0.9
    font_name = 'DejaVu'
    font_size = font_size_base
    while pdfmetrics.stringWidth(random_text, font_name, font_size) > max_width:
        font_size -= 5
    c.setFont(font_name, font_size)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT / 2, random_text)
    c.showPage()

def image_slide(path):
    random_image = random.choice(images[path])
    images[path].remove(random_image)

    c.drawImage(base_dir/'assets'/path/random_image, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT, preserveAspectRatio=True, anchor='c')
    c.showPage()


for t, p in order:
    if t == "t":
        text_slide(p)
    if t == 'i':
        image_slide(p)

c.save()
print('Презентация готова')
