from flask import Flask, jsonify
from pi.db.adsb_database import ADSBDatabase
from pi.analytics.planes_overhead import planes_overhead_now
from pi.analytics.daily import compute_daily_flights
import datetime

app = Flask(__name__)
db = ADSBDatabase("/home/pi/adsb/adsb_data.db")

@app.get("/api/planes/now")
def api_planes_now():
    rows = planes_overhead_now(db)
    return jsonify(rows)

@app.get("/api/stats/daily")
def api_daily():
    today = datetime.date.today()
    rows = compute_daily_flights(db, today)
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
