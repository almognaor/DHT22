import time
import csv
import board
import adafruit_dht

# --- הגדרת החיישן ---
dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# --- קובץ לוג ---
LOG_FILE = "dht22_step_response.csv"
DURATION_MIN = 10             # כמה דקות להריץ
SAMPLE_INTERVAL = 2.0         # *** דגימה כל 2 שניות בהתאם לדאטה-שיט ***
print("Starting DHT22 step-response test...")
print(f"Sampling every {SAMPLE_INTERVAL} seconds for {DURATION_MIN} minutes")
print("once 120 seconds will  pass we will add a heat source")

with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["unix_time", "elapsed_s",
                     "temperature_c", "humidity", "ok"])

    start = time.time()

    while True:
        elapsed = time.time() - start
        if elapsed > DURATION_MIN * 60:
            break

        t = None
        h = None
        ok = 0

        try:
            t = dht.temperature
            h = dht.humidity
            ok = 1
            print(f"{elapsed:6.1f}s -> Temp: {t:4.1f}°C, Humidity: {h:4.1f}%")
        except Exception:
            # אם הייתה שגיאה – ok נשאר 0
            print(f"{elapsed:6.1f}s -> read error")

        writer.writerow([time.time(), elapsed, t, h, ok])

        time.sleep(SAMPLE_INTERVAL)

print("\nStep-response test finished.")
print(f"Data saved to {LOG_FILE}")
