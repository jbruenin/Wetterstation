import time
import dht
from machine import Pin, UART, I2C
from bmp281 import BMP280

# === DHT11 Setup ===
dht_sensor = dht.DHT11(Pin(15))  # DHT11 an GPIO15

# === BMP280 Setup (I2C auf GPIO0 = SDA, GPIO1 = SCL) ===
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

print(i2c.scan())  # Überprüft, welche Adressen verfügbar sind

bmp280_sensor = BMP280(i2c)

# === UART Setup ===
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

while True:
    # --- DHT11 auslesen ---
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
        print("DHT11 → Temp: {}°C, Feuchte: {}%".format(dht_temp, dht_hum))
        uart1.write("Temp: {} °C, Feuchte: {} %\n".format(temp, hum))
        except Exception as e:
        print("DHT11 Fehler:", e)
        uart.write("DHT11 Fehler: {}\n".format(e))

    # --- BMP280 auslesen ---
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
        print("BMP280 → Temp: {:.2f}°C, Druck: {:.2f} hPa".format(bmp_temp, bmp_press))
       
    except Exception as e:
        print("BMP280 Fehler:", e)
        uart.write("BMP280 Fehler: {}\n".format(e))

    if uart1.any():
        incoming = uart1.read().decode('utf-8').strip()
        print("UART empfangen:", incoming)
        uart1.write("Befehl empfangen: {}\n".format(incoming))

    time.sleep(2)