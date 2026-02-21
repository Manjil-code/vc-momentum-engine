import hashlib
from typing import List, Dict

def generate_signal_urls(entity: Dict) -> List[Dict]:
    base = entity["website"].rstrip("/")

    potential_paths = [
        ("hiring", "/careers"),
        ("product_update", "/blog"),
        ("funding", "/news"),
        ("funding", "/press"),
        ("rss", "/feed"),
        ("rss", "/rss")
    ]

    urls = []

    for category, path in potential_paths:
        urls.append({
            "entity_name": entity["name"],
            "entity_url": base,
            "category": category,
            "url": base + path
        })

    return urls


def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
