import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

DB_FILE = "readings.db"

def fetch_last(n=100):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        SELECT time_iso, tempC, thresholdC
        FROM readings
        ORDER BY id DESC
        LIMIT ?
    """, (n,))
    rows = cur.fetchall()
    con.close()
    rows.reverse()
    return rows

def main():
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Live Temperature (from MQTT -> DB)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

    while True:
        rows = fetch_last(200)
        if rows:
            times = [datetime.fromisoformat(r[0]) for r in rows]
            temps = [r[1] for r in rows]
            threshold = rows[-1][2]

            ax.clear()
            ax.set_title("Live Temperature (from MQTT -> DB)")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature (°C)")
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

            ax.plot(times, temps)
            ax.axhline(threshold, linestyle="--")
            fig.autofmt_xdate()
            plt.pause(2)
        else:
            plt.pause(2)

if __name__ == "__main__":
    main()
