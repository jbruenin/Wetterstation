import time
import dht
from machine import Pin, UART, I2C
from bmp281 import BMP280

# === DHT11 Setup ===
dht_sensor = dht.DHT11(Pin(15))  # DHT11 an GPIO15

# === BMP280 Setup (I2C auf GPIO0 = SDA, GPIO1 = SCL) ===
i2c_bmp = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)  # I2C Setup für den BMP280
bmp280_sensor = BMP280(i2c_bmp)

# === UART Setup ===
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# === HM3301 Setup (I2C auf GPIO0 = SDA, GPIO1 = SCL) ===
i2c_hm = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # I2C Setup für den HM3301
HM3301_ADDR = 0x40  # Standardadresse des HM3301

# Funktion zum Auslesen der Feinstaubdaten
def read_hm3301():
    try:
        # Lese 32 Bytes vom HM3301 (ab Adresse 0x00)
        data = i2c_hm.readfrom(HM3301_ADDR, 32)
        
        # PM2.5 und PM10 aus den entsprechenden Bytes extrahieren
        pm25 = (data[4] << 8) | data[5]
        pm10 = (data[6] << 8) | data[7]
        
        print(f"HM3301 → PM2.5: {pm25} µg/m³")
        print(f"HM3301 → PM10: {pm10} µg/m³")

    except Exception as e:
        print("Fehler beim Auslesen des HM3301:", e)

while True:
    # --- DHT11 auslesen ---
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
        print("DHT11 → Temp: {}°C, Feuchte: {}%".format(dht_temp, dht_hum))
        
    except Exception as e:
        print("DHT11 Fehler:", e)
       

    # --- BMP280 auslesen ---
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
        print("BMP280 → Temp: {:.2f}°C, Druck: {:.2f} hPa".format(bmp_temp, bmp_press))
       
    except Exception as e:
        print("BMP280 Fehler:", e)

    # --- UART-Eingabe auslesen und auf "read" reagieren ---
    if uart1.any():
        incoming = uart1.read().decode('utf-8').strip()
        print("UART empfangen:", incoming)
        
        if incoming.lower() == "read":
            try:
                dht_sensor.measure()
                temp = dht_sensor.temperature()
                hum = dht_sensor.humidity()
                print("Temperatur: {} °C, Luftfeuchtigkeit: {} %".format(temp, hum))
            except OSError as e:
                print("Fehler beim DHT11-Auslesen:", e)
        else:
            print("Unbekannter Befehl:", incoming)

    # --- HM3301 Feinstaubdaten auslesen ---
    read_hm3301()

    # Pause zwischen den Messungen
    time.sleep(2)


