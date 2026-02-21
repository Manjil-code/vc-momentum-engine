import aiohttp
import asyncio
from typing import List

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

class AsyncFetcher:
    def __init__(self, concurrency: int = 5, timeout: int = 15):
        self.concurrency = concurrency
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(concurrency)

    async def _fetch(self, session: aiohttp.ClientSession, url: str):
        async with self.semaphore:
            try:
                async with session.get(
                    url,
                    headers=DEFAULT_HEADERS,
                    timeout=self.timeout,
                    allow_redirects=True,
                    ssl=False
                ) as response:
                    if response.status == 200:
                        return await response.text()
                    return None
            except Exception:
                return None

    async def fetch_many(self, urls: List[str]):
        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [self._fetch(session, url) for url in urls]
            return await asyncio.gather(*tasks)
