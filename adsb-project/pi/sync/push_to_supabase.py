import os
import datetime
import sys
from supabase import create_client, Client
from pi.db.adsb_database import ADSBDatabase


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pi.analytics.daily import compute_daily_flights
from pi.analytics.hourly import compute_hourly_flights
from pi.analytics.airlines import compute_airline_stats
from pi.analytics.origins import compute_origin_dest_stats

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def upsert(table: str, rows: list[dict]):
    sb = get_supabase()
    if not rows:
        return
    sb.table(table).upsert(rows).execute()

def run_sync():
    print("[INFO] Running Supabase sync...")
    db = ADSBDatabase(db_path="/home/pi/adsb/adsb_data.db")

    today = datetime.date.today()

    # Compute analytics
    daily = compute_daily_flights(db, today)
    hourly = compute_hourly_flights(db, today)
    airlines = compute_airline_stats(db, today)
    origins = compute_origin_dest_stats(db, today)

    now = datetime.datetime.utcnow().isoformat()

    for row in daily:
        row["updated_at"] = now
    for row in hourly:
        row["updated_at"] = now
    for row in airlines:
        row["updated_at"] = now
    for row in origins:
        row["updated_at"] = now

    upsert("daily_flights", daily)
    upsert("hourly_flights", hourly)
    upsert("airline_stats", airlines)
    upsert("origin_dest_stats", origins)

    print("[INFO] Sync complete.")

if __name__ == "__main__":
    run_sync()
