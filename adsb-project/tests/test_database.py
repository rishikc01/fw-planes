import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.db.adsb_database import ADSBDatabase

db = ADSBDatabase()

sample = {
    "icao": "A1B2C3",
    "callsign": "DAL123",
    "lat": 47.6205,
    "lon": -122.3493,
    "altitude": 3200,
    "speed": 210,
    "heading": 145,
    "timestamp": time.time()
}

db.insert_message(sample)

print(db.get_recent_messages(300))
