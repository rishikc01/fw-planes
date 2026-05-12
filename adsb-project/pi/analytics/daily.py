import datetime

def compute_daily_flights(db, date: datetime.date):
    """
    Returns a list with one row:
    {
        "date": "YYYY-MM-DD",
        "flight_count": <int>
    }
    """
    start = datetime.datetime.combine(date, datetime.time.min).timestamp()
    end = datetime.datetime.combine(date, datetime.time.max).timestamp()

    rows = db.query("""
        SELECT COUNT(DISTINCT icao) AS count
        FROM adsb_messages
        WHERE timestamp BETWEEN ? AND ?
    """, (start, end))

    return [{
        "date": date.isoformat(),
        "flight_count": rows[0]["count"]
    }]
