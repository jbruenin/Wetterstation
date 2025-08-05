import time
import dht
from machine import Pin, UART, I2C
from bmp281 import BMP280

# === DHT22 Setup ===
# IMPORTANT: Change dht.DHT11 to dht.DHT22
dht_sensor = dht.DHT22(Pin(15))  # DHT22 an GPIO15

# === BMP280 Setup (I2C auf GPIO0 = SDA, GPIO1 = SCL) ===
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)

print(i2c.scan())  # Überprüft, welche Adressen verfügbar sind

bmp280_sensor = BMP280(i2c)

# === UART Setup ===
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

while True:
    # --- DHT22 auslesen ---
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
        # DHT22 can provide more precise readings, often with decimals.
        print("DHT22 → Temp: {:.1f}°C, Feuchte: {:.1f}%".format(dht_temp, dht_hum))
        
    except Exception as e:
        print("DHT22 Fehler:", e)
        

    # --- BMP280 auslesen ---
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
        print("BMP280 → Temp: {:.2f}°C, Druck: {:.2f} hPa".format(bmp_temp, bmp_press))
        
    except Exception as e:
        print("BMP280 Fehler:", e)
        

    if uart1.any():
        incoming = uart1.read().decode('utf-8').strip()
        print("UART empfangen:", incoming)
        
        if incoming.lower() == "read":
            try:
                dht_sensor.measure()
                temp = dht_sensor.temperature()
                hum = dht_sensor.humidity()
                # Again, better formatting for DHT22 precision
                print("Temperatur: {:.1f} °C, Luftfeuchtigkeit: {:.1f} %".format(temp, hum))
            except OSError as e:
                print("Fehler beim DHT22-Auslesen:", e)
        else:
            print("Unbekannter Befehl:", incoming)

    time.sleep(2)
    