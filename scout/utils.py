import hashlib


def generate_signal_urls(entity):
    base = entity["entity_url"].rstrip("/")

    potential_paths = [
        ("news", "/news"),
        ("blog", "/blog"),
        ("careers", "/careers"),
        ("funding", "/press"),
    ]

    urls = []

    for category, path in potential_paths:
        urls.append({
            "entity_name": entity["entity_name"],
            "entity_url": entity["entity_url"],
            "category": category,
            "url": base + path
        })

    return urls


def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()
