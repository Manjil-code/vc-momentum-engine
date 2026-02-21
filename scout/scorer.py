def score_signal(text: str, category: str) -> float:
    text = text.lower()

    base_score = 0.2

    keyword_weights = {
        "funding": ["series", "funding", "raised", "investment"],
        "hiring": ["hiring", "open role", "join us", "careers"],
        "product_update": ["launch", "release", "introducing", "new feature"],
        "rss": ["announce", "update", "launch"]
    }

    for keyword in keyword_weights.get(category, []):
        if keyword in text:
            base_score += 0.2

    # Cap at 1.0
    return min(base_score, 1.0)
