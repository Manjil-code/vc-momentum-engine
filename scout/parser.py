from bs4 import BeautifulSoup
from datetime import datetime
from scout.utils import generate_hash
from scout.scorer import score_signal

class SignalParser:

    @staticmethod
    def parse(entity_name: str, entity_url: str, category: str, url: str, html: str):
        if not html:
            return None

        soup = BeautifulSoup(html, "lxml")

        # Extract visible text
        text = soup.get_text(separator=" ", strip=True)

        if len(text) < 300:
            return None

        # Score the signal
        confidence = score_signal(text, category)

        signal_hash = generate_hash(entity_name + category + text[:200])

        return {
            "entity_name": entity_name,
            "entity_url": entity_url,
            "signal_type": category,
            "signal_text": text[:800],
            "signal_date": str(datetime.utcnow().date()),
            "source_url": url,
            "category_tag": category,
            "confidence_score": confidence,
            "scraped_at": str(datetime.utcnow()),
            "signal_hash": signal_hash
        }
