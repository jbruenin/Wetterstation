from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

print("I2C Scan:", i2c.scan())
time.sleep(2)  # Sensor-Startup-Zeit

while True:
    try:
        data = i2c.readfrom(0x40, 29)
        print("RAW:", [hex(b) for b in data])
    except OSError as e:
        print("Fehler:", e)
    time.sleep(2)
