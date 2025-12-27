import time
import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)

while True:
    for attempt in range(5):
        try:
            t = dht.temperature
            h = dht.humidity
            print(f"Temp: {t:.1f}°C, Humidity: {h:.1f}%")
            break 
        except Exception as e:
            time.sleep(0.2)
    time.sleep(3)
