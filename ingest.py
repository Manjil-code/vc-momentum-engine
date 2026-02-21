import requests
import asyncio
import aiohttp
from datetime import datetime
import hashlib
from scout.entity_loader import EntityLoader
from scout.utils import generate_signal_urls
from scout.ai_classifier import classify_signal
from scout.db import get_connection


# ----------------------------------------
# Helpers
# ----------------------------------------

def generate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except Exception:
        return None


async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)


# ----------------------------------------
# Main Ingestion Logic
# ----------------------------------------

async def main():

    print("Initializing ingestion...")

    loader = EntityLoader()
    entities = loader.load()

    all_signal_urls = []

    for entity in entities:
        urls = generate_signal_urls(entity)
        all_signal_urls.extend(urls)

    print(f"Generated {len(all_signal_urls)} signal URLs")

    print("Fetching signals...")
    responses = await fetch_all([u["url"] for u in all_signal_urls])

    print("Parsing and storing signals...")

    conn = get_connection()
    cursor = conn.cursor()

    for meta, content in zip(all_signal_urls, responses):

        if not content:
            continue

        entity_name = meta["entity_name"]
        url = meta["url"]

        # Use first 1000 chars for classification
        signal_text = content[:1000]

        category_tag, confidence_score = classify_signal(signal_text)

        signal_hash = generate_hash(entity_name + url)

        signal_date = datetime.utcnow().strftime("%Y-%m-%d")

        try:
            cursor.execute(
                """
                INSERT INTO signals (
                    signal_hash,
                    entity_name,
                    source_url,
                    category_tag,
                    confidence_score,
                    signal_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    signal_hash,
                    entity_name,
                    url,
                    category_tag,
                    confidence_score,
                    signal_date
                ),
            )
        except Exception:
            # Skip duplicates or insertion errors
            continue

    conn.commit()
    conn.close()

    print("Ingestion complete.")


# ----------------------------------------
# Run
# ----------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
