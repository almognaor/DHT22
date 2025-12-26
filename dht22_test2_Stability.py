import time
import csv
import board
import adafruit_dht

# --- הגדרת החיישן ---
dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# --- קובץ לוג ---
LOG_FILE = "dht22_stability.csv"   # הקובץ ייווצר באותה תיקייה
DURATION_MIN = 10                  # כמה דקות להריץ (שנה ל-30 אח"כ)
SAMPLE_INTERVAL = 2.0              # דגימה כל כמה שניות
MAX_RETRIES = 5                    # מספר ניסיונות לקריאה

print("Starting DHT22 stability test...")
print(f"Sampling every {SAMPLE_INTERVAL} seconds for {DURATION_MIN} minutes")

# --- פתיחת הקובץ וכתיבה ראשונית ---
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

        # --- ניסיונות קריאה ---
        for attempt in range(MAX_RETRIES):
            try:
                t = dht.temperature
                h = dht.humidity
                ok = 1
                print(f"{elapsed:6.1f}s -> Temp: {t:4.1f}°C, Humidity: {h:4.1f}%")
                break
            except Exception:
                time.sleep(0.2)

        # --- כתיבת התוצאה לקובץ ---
        writer.writerow([time.time(), elapsed, t, h, ok])

        # --- זמן המתנה לדגימה הבאה ---
        time.sleep(SAMPLE_INTERVAL)

print("\nTest finished.")
print(f"Data saved to {LOG_FILE}")
