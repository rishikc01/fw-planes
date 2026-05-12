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
