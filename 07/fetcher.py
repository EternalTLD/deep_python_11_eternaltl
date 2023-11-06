from collections import Counter
import asyncio
import re
import time
import aiohttp
from bs4 import BeautifulSoup


async def get_text(url: str) -> str | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            page_text = soup.get_text()
            return page_text
        

def get_most_common_words(text: str, most_common: int) -> dict:
    words = re.findall(r"\b[А-Яа-яA-Za-z]+\b", text.lower())
    most_common_words = Counter(words).most_common(
        most_common
    )
    most_common_words_dict = {}
    for (word, count) in most_common_words:
        most_common_words_dict[word] = count
    return most_common_words_dict


async def fetch_workers(que: asyncio.Queue, most_common: int) -> None:
    while True:
        url = await que.get()
        text = await get_text(url)
        words = get_most_common_words(text, most_common)
        print(f"{url}: {words}")


async def run_fetcher(workers_number: int, urls: list[str], most_common: int) -> None:
    que = asyncio.Queue()

    workers = [
        asyncio.create_task(fetch_workers(que, most_common))
        for _ in range(workers_number)
    ]

    for url in urls:
        await que.put(url)

    await que.join()

    for worker in workers:
        worker.cancel()


if __name__ == "__main__":
    urls = []
    with open("07/urls.txt", "r", encoding="utf-8") as file_object:
        for url in file_object:
            urls.append(url.strip())
    workers_number = 10
    most_common = 7

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_fetcher(workers_number, urls, most_common))
    loop.close()