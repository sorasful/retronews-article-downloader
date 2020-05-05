import asyncio
import sys
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path

import aiofiles
import fire
import httpx
from aiofiles import os
from loguru import logger

from image_utils import reconstruct_article_image


def extract_ids_of_article_url(url: str):
    *_, id1, id2, _ = url.split('/')

    return id1, id2


async def download_image_from_url(url: str, client, filename: str):
    """
    Async function to download and write an image URL to a file.
    :param url: Url of the image to download
    :param client: HTTPX client
    :param filename: Path where to store the image
    :return:
    """
    response = await client.get(url)
    logger.debug(f"Waiting for url {url} {response.status_code}")
    if response.status_code != 200:
        return
    async with aiofiles.open(filename, 'wb') as f:
        await f.write(response.content)


async def download_one_article_page(client, dirname, id1, id2, page):
    """
    Async Function used to download all image that constitue ONE page of an article. Useful if you do not want all
    the article.
    :param client: HTTPX client
    :param dirname: Directory where to store the images
    :param id1: publication_id of the article (the first ID in the end of the url)
    :param id2: Id of the publication (the second ID at the end of the URL)
    :param page: Number of page (starting at 1)
    :return:
    """
    coroutines = []

    # TODO: Optimize calls for column and rows
    for row in range(8):
        for column in range(8):
            filename = f'{id1}-{id2}-{page}-{row}-{column}.jpg'
            path_to_store = dirname / Path(filename)
            url = f"https://pv5web.retronews.fr/api/document/{id1}/{id2}/page/{page}/tile/{column}/{row}/0"
            coroutines.append(download_image_from_url(url=url, client=client, filename=path_to_store))

    logger.info(f"Fetching images for page {page} ...")
    await asyncio.gather(*coroutines)


async def download_full_article(article_url):
    id1, id2 = extract_ids_of_article_url(article_url)
    dirname = f'{id1}-{id2}'

    if not Path(dirname).exists():
        await os.mkdir(dirname)

    async with httpx.AsyncClient(timeout=None) as client:
        # contains information like the number of pages to iterate on
        article_metadata_url = f"https://pv5web.retronews.fr/api/document/{id1}/{id2}"

        article_metadata_response = await client.get(article_metadata_url)
        article_metadata = article_metadata_response.json()

        for page in range(1, article_metadata['nbPages'] + 1):
            await download_one_article_page(client, dirname, id1, id2, page)
            await asyncio.sleep(0.3)

            with ProcessPoolExecutor() as executor:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(executor, reconstruct_article_image, page, dirname)


async def download_page_from_article(article_url: str, page: int):
    id1, id2 = extract_ids_of_article_url(article_url)
    dirname = f'{id1}-{id2}'

    if not Path(dirname).exists():
        await os.mkdir(dirname)

    async with httpx.AsyncClient(timeout=None) as client:
        await download_one_article_page(client, dirname, id1, id2, page)

        with ProcessPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, reconstruct_article_image, page, dirname )


def download_page(article_url: str, page: int):
    """
    Allows to download a specific page into a JPG image from retronews.fr URL.
    :param article_url: The url of the article
    :param page: The page you want to get
    """
    asyncio.get_event_loop().run_until_complete(download_page_from_article(article_url, page=page))


def download_all_pages(article_url: str):
    """
    Allows to download all pages into JPG images from retronews.fr URL.
    :param article_url: The url of the article
    """
    asyncio.get_event_loop().run_until_complete(download_full_article(article_url))


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stderr, format="{time} {level} {message}",  level="INFO")

    fire.Fire({
        'download_page': download_page,
        'download_all_pages': download_all_pages
    })

    logger.info("Program finished.")
