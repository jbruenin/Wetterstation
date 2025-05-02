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
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

while True:
    # --- DHT11 auslesen ---
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
        print("DHT11 → Temp: {}°C, Feuchte: {}%".format(dht_temp, dht_hum))
        uart.write("DHT11 → Temp: {}°C, Feuchte: {}%\n".format(dht_temp, dht_hum))
    except Exception as e:
        print("DHT11 Fehler:", e)
        uart.write("DHT11 Fehler: {}\n".format(e))

    # --- BMP280 auslesen ---
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
        print("BMP280 → Temp: {:.2f}°C, Druck: {:.2f} hPa".format(bmp_temp, bmp_press))
        uart.write("BMP280 → Temp: {:.2f}°C, Druck: {:.2f} hPa\n".format(bmp_temp, bmp_press))
    except Exception as e:
        print("BMP280 Fehler:", e)
        uart.write("BMP280 Fehler: {}\n".format(e))

    # --- UART-Empfang prüfen ---
    if uart.any():
        rx_data = uart.readline()
        if rx_data:
            print("UART empfangen:", rx_data.decode('utf-8').strip())

    time.sleep(2)