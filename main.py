import time
import dht
from machine import Pin
from machine import I2C, Pin
import bme280

# I2C Setup
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Passen ggf. an

# Sensor initialisieren
bme = bme280.BME280(i2c=i2c)

sensor = dht.DHT11(Pin(15))  # Passe Pin an

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("Temperatur: {}°C  Luftfeuchtigkeit: {}%".format(temp, hum))
    except OSError as e:
        print("Fehler beim Lesen:", e)
    # i2c stup
    emp, pres, hum = bme.read_compensated_data()
    print("Temperatur: {:.2f} °C".format(temp / 100))
    print("Luftdruck: {:.2f} hPa".format(pres / 25600))
    print("Luftfeuchtigkeit: {:.2f} %".format(hum / 1024))
    print("-----")
        
    
    time.sleep(2)	