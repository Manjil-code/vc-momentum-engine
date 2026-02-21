import pandas as pd

DEFAULT_ENTITY_FILE = "data_sources/cleaned_global_startups.csv"

class EntityLoader:

    def __init__(self, filepath=DEFAULT_ENTITY_FILE):
        self.filepath = filepath

    def load(self, limit=None):
        df = pd.read_csv(self.filepath)

        if limit:
            df = df.head(limit)

        entities = []

        for _, row in df.iterrows():
            entities.append({
                "entity_name": row["name"],
                "entity_url": row["website"],
                "sector": row["sector"],
                "region": row["region"]
            })

        return entities
