from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import os
import re

directory = Path('437-1806613')
page = 1

images_paths_for_page = sorted([str(x) for x in filter(lambda x: re.search(f"\d+-\d+-{page}-\d+-\d+.jpg", x.name), directory.iterdir())])

# sort the name of the images, get the last one (with biggest row and col)
# then use regex to capture the values
max_col, max_row = map(int, re.search(f"\d+-\d+/\d+-\d+-{page}-(\d+)-(\d+).jpg", images_paths_for_page[-1]).groups())

# images = [Image.open(path) for path in images_paths_for_page]


im0 = Image.open(images_paths_for_page[0])
width, height = map(int, im0.size)

result_img = Image.new('RGB', (width * max_col + 1 ,height * max_row + 1))

for img in images_paths_for_page:
    col, row = map(int, re.search(f"\d+-\d+/\d+-\d+-{page}-(\d+)-(\d+).jpg", img).groups())
    image = Image.open(img)
    result_img.paste(image, (row* width, col * height))

result_img.save('results.jpg')