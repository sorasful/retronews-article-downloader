import re
from pathlib import Path

from PIL import Image


def reconstruct_article_image(page_to_reconstruct: int, directory_holding_images: str):
    """
    Retronews images are cut in row and column, so we need to put them back together in good order.
    """

    directory_holding_images = Path(directory_holding_images)

    # get all the images for a specific page
    images_paths_for_page = sorted([str(x) for x in
                                    filter(lambda x: re.search(f"\d+-\d+-{page_to_reconstruct}-\d+-\d+.jpg", x.name),
                                           directory_holding_images.iterdir())])

    # sort the name of the images, get the last one (with biggest row and col)
    # then use regex to capture the values
    max_col, max_row = map(int, re.search(f"\d+-\d+/\d+-\d+-{page_to_reconstruct}-(\d+)-(\d+).jpg",
                                          images_paths_for_page[-1]).groups())

    im0 = Image.open(images_paths_for_page[0])
    width, height = map(int, im0.size)

    # index of row and col starts at 0, so we need to add 1 to get the good size
    result_img = Image.new('RGB', (width * (max_row + 1), height * (max_col + 1)))

    # paste each image in the good spot
    for img in images_paths_for_page:
        col, row = map(int, re.search(f"\d+-\d+/\d+-\d+-{page_to_reconstruct}-(\d+)-(\d+).jpg", img).groups())
        image = Image.open(img)
        result_img.paste(image, (row * width, col * height))

    result_img.save(f'{directory_holding_images}-{page_to_reconstruct}.jpg')
