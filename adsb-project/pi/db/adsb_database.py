import sqlite3
from typing import Dict, Any, List, Optional

class ADSBDatabase:
    def __init__ (self, db_path: str = 'adsb_data.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()
    

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS adsb_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            icao TEXT,
            callsign TEXT,
            lat REAL,
            lon REAL,
            altitude INTEGER,
            speed REAL,
            heading REAL,
            timestamp REAL
        );
        """)
        self.conn.commit()

    def insert_message(self, msg: Dict[str, Any]):
        self.conn.execute("""
        INSERT INTO adsb_messages
        (icao, callsign, lat, lon, altitude, speed, heading, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            msg.get("icao"),
            msg.get("callsign"),
            msg.get("lat"),
            msg.get("lon"),
            msg.get("altitude"),
            msg.get("speed"),
            msg.get("heading"),
            msg.get("timestamp")
        ))
        self.conn.commit()

    def get_recent_messages(self, seconds: int = 60) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("""
        SELECT icao, callsign, lat, lon, altitude, speed, heading, timestamp
        FROM adsb_messages
        WHERE timestamp >= strftime('%s','now') - ?
        """, (seconds,))
        rows = cur.fetchall()

        return [dict(row) for row in rows]