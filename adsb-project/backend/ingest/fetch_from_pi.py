import requests
import time
from typing import Dict, Any, List
from backend.db.adsb_database import ADSBDatabase

PI_URL = "http://<PI-IP-HERE>:8080/data.json"

def fetch_adsb_data() -> List[Dict[str, Any]]:
    try:
        resp = requests.get(PI_URL, timeout=2)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Error fetching ADS-B data:", e)
        return []

def normalize_aircraft(ac: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "icao": ac.get("hex"),
        "callsign": ac.get("flight", "").strip() or None,
        "lat": ac.get("lat"),
        "lon": ac.get("lon"),
        "altitude": ac.get("altitude"),
        "speed": ac.get("speed"),
        "heading": ac.get("track"),
        "timestamp": time.time()
    }

def run_ingestion_loop():
    db = ADSBDatabase()

    while True:
        aircraft_list = fetch_adsb_data()

        for ac in aircraft_list:
            if ac.get("lat") is None or ac.get("lon") is None:
                continue  # skip incomplete messages

            msg = normalize_aircraft(ac)
            db.insert_message(msg)

        time.sleep(1)

if __name__ == "__main__":
    run_ingestion_loop()
