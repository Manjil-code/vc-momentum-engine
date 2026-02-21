import aiosqlite
import os

DB_PATH = "data/signals.db"

class SignalDatabase:

    @staticmethod
    async def init():
        os.makedirs("data", exist_ok=True)

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_name TEXT,
                    entity_url TEXT,
                    signal_type TEXT,
                    signal_text TEXT,
                    signal_date TEXT,
                    source_url TEXT,
                    category_tag TEXT,
                    confidence_score REAL,
                    scraped_at TEXT,
                    signal_hash TEXT UNIQUE
                )
            """)
            await db.commit()

    @staticmethod
    async def insert(signal: dict):
        async with aiosqlite.connect(DB_PATH) as db:
            try:
                await db.execute("""
                    INSERT INTO signals (
                        entity_name,
                        entity_url,
                        signal_type,
                        signal_text,
                        signal_date,
                        source_url,
                        category_tag,
                        confidence_score,
                        scraped_at,
                        signal_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    signal["entity_name"],
                    signal["entity_url"],
                    signal["signal_type"],
                    signal["signal_text"],
                    signal["signal_date"],
                    signal["source_url"],
                    signal["category_tag"],
                    signal["confidence_score"],
                    signal["scraped_at"],
                    signal["signal_hash"]
                ))

                await db.commit()

            except Exception:
                # Likely duplicate hash
                pass
