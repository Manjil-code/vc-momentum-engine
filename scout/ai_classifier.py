from transformers import pipeline

# Load once at startup (important for performance)
classifier = pipeline("zero-shot-classification")

LABELS = [
    "funding",
    "hiring",
    "product launch",
    "acquisition",
    "partnership",
    "market expansion",
    "regulation",
    "general news"
]


def classify_signal(text):
    if not text or len(text.strip()) == 0:
        return "general news", 0.5

    result = classifier(text, LABELS)

    top_label = result["labels"][0]
    confidence = float(result["scores"][0])

    return top_label, round(confidence, 3)
