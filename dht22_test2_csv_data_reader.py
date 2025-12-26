import csv
import statistics as stats
import matplotlib.pyplot as plt

# ------------------------------
#         Read CSV Data
# ------------------------------
times = []
temps = []
hums = []
errors = 0
total_samples = 0

with open("dht22_stability.csv") as f:
    reader = csv.DictReader(f)
    for r in reader:
        total_samples += 1

        # אם הקריאה נכשלה (ok=0)
        if r["ok"] != "1":
            errors += 1
            continue

        # אם הערכים ריקים – לדלג
        if r["temperature_c"] == "" or r["humidity"] == "":
            errors += 1
            continue

        try:
            t = float(r["temperature_c"])
            h = float(r["humidity"])
            ts = float(r["elapsed_s"])
        except ValueError:
            errors += 1
            continue

        temps.append(t)
        hums.append(h)
        times.append(ts)

# ------------------------------
#      Statistical Analysis
# ------------------------------

if temps:
    temp_mean = stats.mean(temps)
    temp_std  = stats.pstdev(temps)
    temp_min  = min(temps)
    temp_max  = max(temps)
else:
    temp_mean = temp_std = temp_min = temp_max = None

if hums:
    hum_mean = stats.mean(hums)
    hum_std  = stats.pstdev(hums)
    hum_min  = min(hums)
    hum_max  = max(hums)
else:
    hum_mean = hum_std = hum_min = hum_max = None

error_rate = (errors / total_samples) * 100 if total_samples > 0 else 0

# ------------------------------
#            Print Report
# ------------------------------

print("\n======== DHT22 ANALYSIS REPORT ========")
print(f"Total samples:       {total_samples}")
print(f"Valid samples:       {len(temps)}")
print(f"Error samples:       {errors}")
print(f"Error rate:          {error_rate:.2f}%")

print("\n--- Temperature (°C) ---")
print(f"Mean:                {temp_mean:.3f}")
print(f"Std Dev:             {temp_std:.3f}")
print(f"Min:                 {temp_min}")
print(f"Max:                 {temp_max}")

print("\n--- Humidity (%) ---")
print(f"Mean:                {hum_mean:.3f}")
print(f"Std Dev:             {hum_std:.3f}")
print(f"Min:                 {hum_min}")
print(f"Max:                 {hum_max}")

# ------------------------------
#           Plot Graphs
# ------------------------------

plt.figure(figsize=(10,4))
plt.plot(times, temps, label="Temperature (°C)")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Temperature vs Time")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,4))
plt.plot(times, hums, label="Humidity (%)", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Humidity (%)")
plt.title("Humidity vs Time")
plt.grid(True)
plt.tight_layout()
plt.show()
