import time
import dht
from machine import Pin

sensor = dht.DHT11(Pin(15))  # Passe Pin an

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temperatur: {}°C  Luftfeuchtigkeit: {}%".format(temp, hum))
    except OSError as e:
        print("Fehler beim Lesen:", e)
    
    time.sleep(2)