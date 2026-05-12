import time
from typing import List, Dict, Any
from backend.db.adsb_database import ADSBDatabase

def planes_overhead_now(db: ADSBDatabase, window_seconds: int = 30) -> List[Dict[str, Any]]:
    """
    Returns all aircraft seen in the last `window_seconds`.
    This represents "planes overhead right now".
    """
    current_time = time.time()
    cutoff = current_time - window_seconds

    cur = db.conn.cursor()
    cur.execute("""
        SELECT icao, callsign, lat, lon, altitude, speed, heading, timestamp
        FROM adsb_messages
        WHERE timestamp >= ?
    """, (cutoff,))

    rows = cur.fetchall()
    return [dict(row) for row in rows]
