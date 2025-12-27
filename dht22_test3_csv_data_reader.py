import csv
import statistics as stats
import matplotlib.pyplot as plt

FILENAME = "dht22_step_response.csv"

times = []
temps = []
hums = []
errors = 0
total_samples = 0

# ------------------------------
#   Read CSV data
# ------------------------------
with open(FILENAME) as f:
    reader = csv.DictReader(f)
    for r in reader:
        total_samples += 1

        if r["ok"] != "1":
            errors += 1
            continue

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
#   Basic statistics
# ------------------------------
def safe_stats(data):
    if len(data) == 0:
        return None, None, None, None
    return stats.mean(data), stats.pstdev(data), min(data), max(data)

temp_mean, temp_std, temp_min, temp_max = safe_stats(temps)
hum_mean, hum_std, hum_min, hum_max = safe_stats(hums)
error_rate = (errors / total_samples) * 100 if total_samples else 0

# ------------------------------
#   Step Response Analysis
# ------------------------------

# 1) Detect start temperature (before step)
baseline_duration = 120   # first 120 seconds baseline
baseline_temps = [temps[i] for i in range(len(times)) if times[i] <= baseline_duration]

T_initial = stats.mean(baseline_temps)
T_final = max(temps)  # assume max is the final value after heating

deltaT = T_final - T_initial

# Values for response time
target_t90 = T_initial + 0.90 * deltaT
target_tau = T_initial + 0.632 * deltaT
target_settle_low = T_initial + 0.98 * deltaT
target_settle_high = T_initial + 1.02 * deltaT

t90_time = None
tau_time = None
settling_time = None

for i in range(len(temps)):
    T = temps[i]

    # Time constant τ (63.2% rise)
    if tau_time is None and T >= target_tau:
        tau_time = times[i]

    # t90 response time (90% rise)
    if t90_time is None and T >= target_t90:
        t90_time = times[i]

    # Settling time (within ±2% of final value)
    if T >= target_settle_low and T <= target_settle_high:
        if settling_time is None:
            settling_time = times[i]

# Convert relative times (subtract baseline start)
if tau_time: tau_time -= baseline_duration
if t90_time: t90_time -= baseline_duration
if settling_time: settling_time -= baseline_duration

# ------------------------------
#        PRINT RESULTS
# ------------------------------
print("\n======== DHT22 STEP RESPONSE ANALYSIS ========")
print(f"Total samples:       {total_samples}")
print(f"Valid samples:       {len(temps)}")
print(f"Error samples:       {errors}")
print(f"Error rate:          {error_rate:.2f}%\n")

print("--- Temperature (°C) Stats ---")
print(f"Initial temp:        {T_initial:.3f}")
print(f"Final temp:          {T_final:.3f}")
print(f"ΔTemp:               {deltaT:.3f}\n")

print("--- Response Metrics ---")
print(f"Time Constant τ:     {tau_time:.2f} seconds")
print(f"t90 Response Time:   {t90_time:.2f} seconds")
print(f"Settling Time:       {settling_time:.2f} seconds\n")

print("--- Humidity (%) Stats ---")
print(f"Mean:                {hum_mean:.3f}")
print(f"Std Dev:             {hum_std:.3f}")
print(f"Min:                 {hum_min}")
print(f"Max:                 {hum_max}\n")

# ------------------------------
#     PLOT GRAPHS
# ------------------------------
plt.figure(figsize=(10,4))
plt.plot(times, temps, color="red")
plt.axhline(T_initial, linestyle='--', color='gray', label="Initial")
plt.axhline(T_final, linestyle='--', color='black', label="Final")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("DHT22 Step Response – Temperature vs Time")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,4))
plt.plot(times, hums, color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Humidity (%)")
plt.title("DHT22 Step Response – Humidity vs Time")
plt.grid(True)
plt.tight_layout()
plt.show()
