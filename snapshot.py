from datetime import datetime
from scout.ranking import MomentumRanking
from scout.db import get_connection

def save_snapshot():
    ranked = MomentumRanking.compute()

    if ranked.empty:
        print("No ranking data available.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.utcnow().strftime("%Y-%m-%d")

    for _, row in ranked.iterrows():
        cursor.execute(
            """
            INSERT INTO momentum_history (entity_name, momentum_score, snapshot_date)
            VALUES (?, ?, ?)
            """,
            (
                row["entity_name"],
                row["momentum_score"],
                today
            )
        )

    conn.commit()
    conn.close()

    print("Snapshot saved successfully.")


if __name__ == "__main__":
    save_snapshot()
