import datetime

def compute_hourly_flights(db, date: datetime.date):
    """
    Returns rows like:
    {
        "date": "YYYY-MM-DD",
        "hour": 0-23,
        "flight_count": <int>
    }
    """
    results = []

    for hour in range(24):
        start_dt = datetime.datetime.combine(date, datetime.time(hour=hour, minute=0))
        end_dt = start_dt + datetime.timedelta(hours=1)

        start = start_dt.timestamp()
        end = end_dt.timestamp()

        rows = db.query("""
            SELECT COUNT(DISTINCT icao) AS count
            FROM adsb_messages
            WHERE timestamp BETWEEN ? AND ?
        """, (start, end))

        results.append({
            "date": date.isoformat(),
            "hour": hour,
            "flight_count": rows[0]["count"]
        })

    return results
