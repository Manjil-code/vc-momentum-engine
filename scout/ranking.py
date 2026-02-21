import sqlite3
from datetime import datetime
import pandas as pd


DB_PATH = "data/signals.db"


class MomentumRanking:

    @staticmethod
    def compute():
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM signals", conn)

        if df.empty:
            return pd.DataFrame()

        df["signal_date"] = pd.to_datetime(df["signal_date"])
        df["days_old"] = (datetime.utcnow() - df["signal_date"]).dt.days

        # Recency bonus
        df["recency_bonus"] = df["days_old"].apply(
            lambda x: 0.3 if x <= 7 else (0.15 if x <= 30 else 0)
        )

        # Base score
        df["weighted_score"] = df["confidence_score"] + df["recency_bonus"]

        grouped = df.groupby("entity_name")

        results = []

        for name, group in grouped:
            base_score = group["weighted_score"].sum()
            diversity_bonus = len(group["category_tag"].unique()) * 0.2
            signal_count = len(group)

            total_score = base_score + diversity_bonus + (signal_count * 0.05)

            results.append({
                "entity_name": name,
                "momentum_score": round(total_score, 2),
                "signal_count": signal_count,
                "last_signal": group["signal_date"].max()
            })

        ranked_df = pd.DataFrame(results)
        ranked_df = ranked_df.sort_values(by="momentum_score", ascending=False)

        return ranked_df
