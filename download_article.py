import asyncio
import sys
from pathlib import Path

import aiofiles
import httpx
from loguru import logger


def extract_ids_of_article_url(url: str):
    *_, id1, id2, _ = url.split('/')

    return id1, id2


async def main(article_url: str):
    id1, id2 = extract_ids_of_article_url(article_url)
    async with httpx.AsyncClient() as client:
        dirname = f'{id1}-{id2}'
        if not Path(dirname).exists():
            await aiofiles.os.mkdir(dirname)

        coroutines = []
        # TODO: Optimize calls
        for page in range(1, 10):
            for row in range(10):
                for column in range(10):
                    filename = f'{id1}-{id2}-{page}-{row}-{column}.jpg'
                    path_to_store = dirname / Path(filename)
                    url = f"https://pv5web.retronews.fr/api/document/{id1}/{id2}/page/{page}/tile/{column}/{row}/0"
                    coroutines.append(download_image_from_url(url=url, client=client, filename=path_to_store))

        logger.info(f"Gathering coroutines ...")
        await asyncio.gather(*coroutines)


async def download_image_from_url(url: str, client, filename: str):
    response = await client.get(url)
    if response.status_code != 200:
        return
    async with aiofiles.open(filename, 'wb') as f:
        await f.write(response.content)


if __name__ == '__main__':
    # https://github.com/encode/httpx/issues/914
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    article_url = "https://www.retronews.fr/journal/le-petit-marseillais/24-mars-1938/437/1806613/1"
    asyncio.run(main(article_url=article_url))

    logger.info("Program finished.")
