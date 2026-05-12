import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pi.db.adsb_database import ADSBDatabase

from pi.analytics.planes_overhead import planes_overhead_now

db = ADSBDatabase()

# Insert a "current" plane
db.insert_message({
    "icao": "ABC123",
    "callsign": "TEST1",
    "lat": 47.62,
    "lon": -122.35,
    "altitude": 3000,
    "speed": 200,
    "heading": 150,
    "timestamp": time.time()
})

# Insert an "old" plane (should NOT show up)
db.insert_message({
    "icao": "OLD999",
    "callsign": "TEST2",
    "lat": 47.60,
    "lon": -122.30,
    "altitude": 2500,
    "speed": 180,
    "heading": 90,
    "timestamp": time.time() - 120  # 2 minutes ago
})

planes = planes_overhead_now(db, window_seconds=30)
print(planes)
