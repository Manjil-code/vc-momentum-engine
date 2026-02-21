import pandas as pd
from typing import List, Dict


class EntityLoader:
    def __init__(self, path: str = "entities.csv"):
        self.path = path

    def load(self, limit: int = 100) -> List[Dict]:
        df = pd.read_csv(self.path)
        df = df.dropna(subset=["name", "website"])
        df = df.head(limit)

        entities = []

        for _, row in df.iterrows():
            entities.append({
                "name": row["name"].strip(),
                "website": row["website"].strip().rstrip("/")
            })

        return entities
