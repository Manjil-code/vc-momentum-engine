import asyncio

from scout.entity_loader import EntityLoader
from scout.fetcher import AsyncFetcher
from scout.parser import SignalParser
from scout.database import SignalDatabase
from scout.utils import generate_signal_urls


async def main():
    print("Initializing database...")
    await SignalDatabase.init()

    loader = EntityLoader()
    entities = loader.load(20)

    fetcher = AsyncFetcher(concurrency=5)

    all_signal_targets = []

    for entity in entities:
        urls = generate_signal_urls(entity)
        all_signal_targets.extend(urls)

    print(f"Generated {len(all_signal_targets)} signal URLs")

    urls_only = [item["url"] for item in all_signal_targets]

    print("Fetching signals...")
    html_results = await fetcher.fetch_many(urls_only)

    print("Parsing and storing signals...")

    for i, html in enumerate(html_results):
        target = all_signal_targets[i]

        signal = SignalParser.parse(
            entity_name=target["entity_name"],
            entity_url=target["entity_url"],
            category=target["category"],
            url=target["url"],
            html=html
        )

        if signal:
            await SignalDatabase.insert(signal)

    print("Ingestion complete.")


if __name__ == "__main__":
    asyncio.run(main())
