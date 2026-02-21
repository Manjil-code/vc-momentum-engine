from datetime import datetime
import pandas as pd
import numpy as np
from scout.entity_loader import EntityLoader
from scout.db import get_connection

CATEGORY_WEIGHTS = {
    "funding": 1.5,
    "hiring": 1.2,
    "product launch": 1.3,
    "acquisition": 1.4,
    "partnership": 1.2,
    "market expansion": 1.1,
    "regulation": 1.0,
    "general news": 0.9
}

LAMBDA = 0.05


class MomentumRanking:

    # -----------------------------------
    # Core Momentum Calculation
    # -----------------------------------

    @staticmethod
    def compute():
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM signals", conn)
        conn.close()

        if df.empty:
            return pd.DataFrame()

        df["signal_date"] = pd.to_datetime(df["signal_date"], errors="coerce")
        df["days_old"] = (datetime.utcnow() - df["signal_date"]).dt.days.fillna(0)

        df["time_decay"] = np.exp(-LAMBDA * df["days_old"])
        df["category_weight"] = df["category_tag"].map(CATEGORY_WEIGHTS).fillna(1.0)

        df["weighted_signal"] = (
            df["confidence_score"]
            * df["category_weight"]
            * df["time_decay"]
        )

        grouped = df.groupby("entity_name")

        results = []

        for name, group in grouped:
            total_score = group["weighted_signal"].sum()
            diversity_bonus = len(group["category_tag"].unique()) * 0.3
            final_score = total_score + diversity_bonus

            results.append({
                "entity_name": name,
                "momentum_score": round(final_score, 3),
                "signal_count": len(group),
                "diversity": len(group["category_tag"].unique()),
                "last_signal": group["signal_date"].max()
            })

        ranked_df = pd.DataFrame(results)
        ranked_df = ranked_df.sort_values(by="momentum_score", ascending=False)

        return ranked_df

    # -----------------------------------
    # Sector Momentum
    # -----------------------------------

    @staticmethod
    def sector_momentum():
        ranked = MomentumRanking.compute()
        if ranked.empty:
            return pd.DataFrame()

        loader = EntityLoader()
        entity_df = pd.DataFrame(loader.load())

        merged = ranked.merge(entity_df, on="entity_name")

        return (
            merged.groupby("sector")["momentum_score"]
            .mean()
            .reset_index()
            .sort_values(by="momentum_score", ascending=False)
        )

    # -----------------------------------
    # Region Momentum
    # -----------------------------------

    @staticmethod
    def region_momentum():
        ranked = MomentumRanking.compute()
        if ranked.empty:
            return pd.DataFrame()

        loader = EntityLoader()
        entity_df = pd.DataFrame(loader.load())

        merged = ranked.merge(entity_df, on="entity_name")

        return (
            merged.groupby("region")["momentum_score"]
            .mean()
            .reset_index()
            .sort_values(by="momentum_score", ascending=False)
        )

    # -----------------------------------
    # Recent Movers
    # -----------------------------------

    @staticmethod
    def recent_movers(days=7):
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM signals", conn)
        conn.close()

        if df.empty:
            return pd.DataFrame()

        df["signal_date"] = pd.to_datetime(df["signal_date"], errors="coerce")
        cutoff = datetime.utcnow() - pd.Timedelta(days=days)

        recent_df = df[df["signal_date"] >= cutoff]

        if recent_df.empty:
            return pd.DataFrame()

        recent_df["category_weight"] = recent_df["category_tag"].map(CATEGORY_WEIGHTS).fillna(1.0)

        recent_df["weighted"] = (
            recent_df["confidence_score"]
            * recent_df["category_weight"]
        )

        return (
            recent_df.groupby("entity_name")["weighted"]
            .sum()
            .reset_index()
            .sort_values(by="weighted", ascending=False)
            .head(10)
        )

    # -----------------------------------
    # Breakout Detection (Ratio-Based)
    # -----------------------------------

    @staticmethod
    def breakout_candidates():
        full = MomentumRanking.compute()
        recent = MomentumRanking.recent_movers(days=7)

        if full.empty or recent.empty:
            return pd.DataFrame()

        merged = recent.merge(full, on="entity_name")

        merged["breakout_ratio"] = (
            merged["weighted"] / merged["momentum_score"]
        )

        breakout = merged[merged["breakout_ratio"] > 0.5]

        return breakout.sort_values(by="breakout_ratio", ascending=False)

    # -----------------------------------
    # Statistical Anomaly Detection (Z-Score)
    # -----------------------------------

    @staticmethod
    def statistical_anomalies():
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM momentum_history", conn)
        conn.close()

        if df.empty:
            return pd.DataFrame()

        df["snapshot_date"] = pd.to_datetime(df["snapshot_date"])

        anomalies = []

        for name, group in df.groupby("entity_name"):

            if len(group) < 5:
                continue

            group = group.sort_values("snapshot_date")

            mean = group["momentum_score"].mean()
            std = group["momentum_score"].std()

            latest = group.iloc[-1]["momentum_score"]

            if std == 0 or pd.isna(std):
                continue

            z_score = (latest - mean) / std

            if z_score > 2:
                anomalies.append({
                    "entity_name": name,
                    "z_score": round(z_score, 2),
                    "current_score": latest
                })

        return (
            pd.DataFrame(anomalies)
            .sort_values(by="z_score", ascending=False)
            if anomalies else pd.DataFrame()
        )
