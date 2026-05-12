# all placeholder logic for computing origin/destination
# idk how to do this well without a real database of callsigns -> airports

import datetime

def compute_origin_dest_stats(db, date: datetime.date):
    """
    Placeholder version:
    Treats airline prefix as 'origin' for now.
    You can upgrade this later with real airport inference.
    """
    start = datetime.datetime.combine(date, datetime.time.min).timestamp()
    end = datetime.datetime.combine(date, datetime.time.max).timestamp()

    rows = db.query("""
        SELECT callsign
        FROM adsb_messages
        WHERE timestamp BETWEEN ? AND ?
    """, (start, end))

    freq = {}

    for row in rows:
        cs = row["callsign"]
        if not cs:
            continue
        prefix = cs[:3].upper()
        freq[prefix] = freq.get(prefix, 0) + 1

    return [
        {
            "date": date.isoformat(),
            "airport": prefix,
            "direction": "origin",
            "count": count
        }
        for prefix, count in freq.items()
    ]
