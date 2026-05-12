import time

def planes_overhead_now(db, window_seconds: int = 60):
    """
    Returns all aircraft seen in the last <window_seconds>.
    """
    cutoff = time.time() - window_seconds

    rows = db.query("""
        SELECT *
        FROM adsb_messages
        WHERE timestamp >= ?
        ORDER BY timestamp DESC
    """, (cutoff,))

    return rows
