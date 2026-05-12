import requests
import time
import traceback
from typing import Dict, Any, List
from pi.db.adsb_database import ADSBDatabase

# dump1090-fa exposes live aircraft JSON here:
DUMP1090_URL = "http://127.0.0.1:8080/data.json"

def fetch_adsb_data() -> List[Dict[str, Any]]:
    """
    Fetches the live aircraft list from dump1090.
    Returns an empty list on failure (so the loop keeps running).
    """
    try:
        resp = requests.get(DUMP1090_URL, timeout=2)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[WARN] Failed to fetch ADS-B data: {e}")
        return []

def normalize(ac: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert dump1090's aircraft JSON into your normalized schema.
    """
    return {
        "icao": ac.get("hex"),
        "callsign": (ac.get("flight") or "").strip() or None,
        "lat": ac.get("lat"),
        "lon": ac.get("lon"),
        "altitude": ac.get("altitude"),
        "speed": ac.get("speed"),
        "heading": ac.get("track"),
        "timestamp": time.time()
    }

def run_ingest_loop():
    print("[INFO] Starting ADS-B ingestion loop...")
    db = ADSBDatabase(db_path="/home/pi/adsb/adsb_data.db")

    while True:
        try:
            aircraft_list = fetch_adsb_data()

            for ac in aircraft_list:
                if ac.get("lat") is None or ac.get("lon") is None:
                    continue

                msg = normalize(ac)
                db.insert_message(msg)

            time.sleep(1)

        except Exception:
            print("[ERROR] Unexpected exception in ingestion loop:")
            traceback.print_exc()
            time.sleep(2)

if __name__ == "__main__":
    run_ingest_loop()
