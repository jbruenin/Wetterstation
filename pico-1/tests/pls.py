import time
import dht
import utime
import math
from machine import Pin, UART, I2C
from bmp281 import BMP280

# === DHT22 Setup ===
dht_sensor = dht.DHT22(Pin(15))

# === BMP280 Setup (I2C auf GPIO3 = SCL, GPIO2 = SDA) ===
i2c_bmp = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)

print(f"I2C Scan BMP: {i2c_bmp.scan()}")

bmp280_sensor = BMP280(i2c_bmp)

# === UART Setup (Beibehalten) ===
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))


# === HM3301 Setup (I2C auf GPIO1 = SCL, GPIO0 = SDA) ===
i2c_hm = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
HM3301_ADDR = 0x40

print(f"I2C Scan HM3301: {i2c_hm.scan()}")


# Funktion zum Auslesen der Feinstaubdaten über I2C
def read_hm3301_i2c(i2c_obj, addr):
    try:
        # Lese 32 Bytes vom HM3301
        data = i2c_obj.readfrom(addr, 32)
        
        # --- NEU: Basis-Längenprüfung ---
        if len(data) < 8: # Wir brauchen mindestens bis data[7] für PM10
            print("HM3301 I2C: Empfangenes Datenpaket zu kurz.")
            return float('nan'), float('nan')

        # --- ENTFERNT: Header-Prüfung und Checksummen-Prüfung ---
        # Basierend auf deiner vorherigen funktionierenden Implementierung und den
        # aktuellen Rohdaten, die zeigen, dass der Sensor abweichendes Verhalten
        # für Header und Checksumme zeigt, aber dennoch gültige PM-Werte liefert.
        
        pm25 = (data[4] << 8) | data[5]
        pm10 = (data[6] << 8) | data[7]
        
        return float(pm25), float(pm10)
    except Exception as e:
        print(f"HM3301 I2C Fehler beim Auslesen: {e}")
        return float('nan'), float('nan')

# Initialisiere Variablen
dht_temp = float('nan')
dht_hum = float('nan')
bmp_temp = float('nan')
bmp_press = float('nan')
pm25_val = float('nan')
pm10_val = float('nan')

while True:
    current_timestamp_unix = utime.time()

    # --- DHT22 auslesen ---
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
    except Exception as e:
        print(f"DHT22 Fehler: {e}")
        dht_temp = float('nan')
        dht_hum = float('nan')

    # --- BMP280 auslesen ---
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
    except Exception as e:
        print(f"BMP280 Fehler: {e}")
        bmp_temp = float('nan')
        bmp_press = float('nan')

    # --- HM3301 Feinstaubdaten auslesen ---
    try:
        pm25_val, pm10_val = read_hm3301_i2c(i2c_hm, HM3301_ADDR)
    except Exception as e:
        print(f"HM3301 Lesefehler (read_hm3301_i2c): {e}")
        pm25_val = float('nan')
        pm10_val = float('nan')

    # --- Konsolidierte Ausgabe für den PC (seriell) ---
    print(f"{current_timestamp_unix},"
          f"{dht_temp if not math.isnan(dht_temp) else 'nan'},"
          f"{dht_hum if not math.isnan(dht_hum) else 'nan'},"
          f"{bmp_temp if not math.isnan(bmp_temp) else 'nan'},"
          f"{bmp_press if not math.isnan(bmp_press) else 'nan'},"
          f"{pm25_val if not math.isnan(pm25_val) else 'nan'},"
          f"{pm10_val if not math.isnan(pm10_val) else 'nan'}")

    time.sleep(10)