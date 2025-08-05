import machine
import utime
import time # Importieren, falls nicht schon oben vorhanden (für time.time())
import dht
from machine import Pin, UART, I2C
from bmp281 import BMP280 # Stellen Sie sicher, dass diese Bibliothek auf Ihrem Pico ist!

# === Hall-Sensor / Geschwindigkeitsmessung Setup ===
hall_sensor_adc = machine.ADC(26) # Hall-Sensor an GPIO 26 (Analog)

# Kalibrierungswerte für die Magneterkennung. ANPASSEN!
# Bestimme diese Werte, indem du den Sensorwert ausgibst (siehe unten) und den Magneten bewegst.
TRIGGER_THRESHOLD = 40000 # Beispiel: Schwellenwert, der einen Magneten anzeigt
DEBOUNCE_TIME_MS = 150    # Entprellzeit in ms. Länger als ein "Prellen", kürzer als halbe Umdrehung.

# Radumfang in cm. ANPASSEN!
wheel_circumference_cm = 200

# Globale Variablen für die Geschwindigkeitsmessung
last_magnet_time = 0
revolutions = 0
current_speed_kmh = 0.0 # Variable, die die aktuelle Geschwindigkeit speichert
magnet_currently_detected = False

# === DHT22 Setup ===
dht_sensor = dht.DHT22(Pin(15)) # DHT22 an GPIO15

# === BMP280 Setup (I2C auf GPIO3 = SCL, GPIO2 = SDA) ===
i2c_bmp = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
bmp280_sensor = BMP280(i2c_bmp)

# === HM3301 Setup (I2C auf GPIO1 = SCL, GPIO0 = SDA) ===
i2c_hm3301 = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
HM3301_ADDR = 0x40

# === UART Setup ===
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Funktion zum Auslesen der Feinstaubdaten
def read_hm3301(i2c_bus):
    pm25 = None
    pm10 = None
    try:
        data = i2c_bus.readfrom(HM3301_ADDR, 32)
        # Checksumme hier ausgelassen, da dein Originalcode sie auch nicht vollständig prüft
        pm25 = (data[4] << 8) | data[5]
        pm10 = (data[6] << 8) | data[7]
    except Exception as e:
        # print("Fehler beim Auslesen des HM3301:", e) # Nur für Debugging, sonst auskommentieren
        pass
    return pm25, pm10

# --- Hauptschleife ---
while True:
    # --- Hall-Sensor / Geschwindigkeitsmessung ---
    hall_value = hall_sensor_adc.read_u16()

    # Optinales Debugging des Hall-Sensor-Werts:
    # print(f"Hall-Sensorwert: {hall_value}")

    if hall_value >= TRIGGER_THRESHOLD and not magnet_currently_detected:
        current_event_time = utime.ticks_ms()
        time_since_last_event = utime.ticks_diff(current_event_time, last_magnet_time)

        if time_since_last_event > DEBOUNCE_TIME_MS:
            revolutions += 1
            last_magnet_time = current_event_time

            if time_since_last_event > 0:
                speed_cm_per_sec = wheel_circumference_cm / (time_since_last_event / 1000)
                current_speed_kmh = speed_cm_per_sec * 0.036
            else:
                current_speed_kmh = 0.0 # Falls time_since_last_event 0 ist

        magnet_currently_detected = True # Magnet wird noch erkannt oder ist im Erkennungsbereich

    elif hall_value < (TRIGGER_THRESHOLD - 5000) and magnet_currently_detected: # Hysterese
        magnet_currently_detected = False # Magnet ist nicht mehr im Erkennungsbereich

    # Wenn das Rad stillsteht oder sich sehr langsam dreht, könnte der
    # time_since_last_event sehr groß werden. Setze die Geschwindigkeit auf 0,
    # wenn längere Zeit kein Signal kam.
    if utime.ticks_diff(utime.ticks_ms(), last_magnet_time) > 2000: # 2 Sekunden Inaktivität
        current_speed_kmh = 0.0

    # --- DHT22 Messung ---
    dht_temp = None
    dht_hum = None
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
    except Exception as e:
        pass

    # --- BMP280 Messung ---
    bmp_temp = None
    bmp_press = None
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
    except Exception as e:
        pass

    # --- HM3301 Messung ---
    hm3301_pm25 = None
    hm3301_pm10 = None
    hm3301_pm25, hm3301_pm10 = read_hm3301(i2c_hm3301)

    # --- UART1 Kommunikation (wie in deinem Originalcode) ---
    if uart1.any():
        incoming = uart1.read().decode('utf-8').strip()
        print("UART empfangen:", incoming)

        if incoming.lower() == "read":
            try:
                if dht_temp is not None and dht_hum is not None:
                    print("Temperatur: {:.1f} °C, Luftfeuchtigkeit: {:.1f} %".format(dht_temp, dht_hum))
                else:
                    dht_sensor.measure() # Fallback
                    temp_uart = dht_sensor.temperature()
                    hum_uart = dht_sensor.humidity()
                    print("Temperatur: {:.1f} °C, Luftfeuchtigkeit: {:.1f} %".format(temp_uart, hum_uart))
            except OSError as e:
                print("Fehler beim DHT22-Auslesen für UART-Befehl:", e)
        else:
            print("Unbekannter Befehl:", incoming)

    # --- DATENZEILE FÜR DEN PC PLOT ---
    # Füge die aktuelle Geschwindigkeit (current_speed_kmh) als neues Datenfeld hinzu.
    # Wichtig: Die Reihenfolge muss im PC-Skript beachtet werden!
    data_line = "{},{},{},{},{},{},{},{}".format(
        time.time(), # Zeitstempel
        current_speed_kmh, # NEU: Geschwindigkeit
        dht_temp if dht_temp is not None else "N/A",
        dht_hum if dht_hum is not None else "N/A",
        bmp_temp if bmp_temp is not None else "N/A",
        bmp_press if bmp_press is not None else "N/A",
        hm3301_pm25 if hm3301_pm25 is not None else "N/A",
        hm3301_pm10 if hm3301_pm10 is not None else "N/A"
    )
    print(data_line)

    utime.sleep_ms(500) # Häufigkeit der Datenübertragung anpassen (alle 0.5 Sekunden)