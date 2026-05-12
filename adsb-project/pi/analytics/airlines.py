import datetime

def extract_airline(callsign: str | None):
    """
    Extracts airline prefix from callsign.
    Example: 'DAL123' -> 'DAL'
    """
    if not callsign:
        return None
    return callsign[:3].upper()

def compute_airline_stats(db, date: datetime.date):
    """
    Returns rows like:
    {
        "date": "YYYY-MM-DD",
        "airline": "DAL",
        "count": <int>
    }
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
        airline = extract_airline(row["callsign"])
        if not airline:
            continue
        freq[airline] = freq.get(airline, 0) + 1

    return [
        {
            "date": date.isoformat(),
            "airline": airline,
            "count": count
        }
        for airline, count in freq.items()
    ]
