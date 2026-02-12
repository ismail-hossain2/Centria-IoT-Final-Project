import json
import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "centria/iot/ismail/temperature"

DB_FILE = "readings.db"

def init_db():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_iso TEXT NOT NULL,
            tempC REAL NOT NULL,
            thresholdC REAL NOT NULL,
            device TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def insert_reading(tempC: float, thresholdC: float, device: str):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO readings (time_iso, tempC, thresholdC, device) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(timespec="seconds"), tempC, thresholdC, device)
    )
    con.commit()
    con.close()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code:", rc)
    client.subscribe(TOPIC)
    print("Subscribed to:", TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        tempC = float(data.get("tempC"))
        thresholdC = float(data.get("thresholdC", 28.0))
        device = str(data.get("device", "unknown"))

        insert_reading(tempC, thresholdC, device)
        print(f"Saved: tempC={tempC:.2f} thresholdC={thresholdC:.2f} device={device}")
    except Exception as e:
        print("Failed to parse/save message:", e, "payload=", msg.payload)

def main():
    init_db()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
