import time
import dht
from machine import Pin, UART, I2C
from bmp281 import BMP280

# === DHT22 Setup ===
dht_sensor = dht.DHT22(Pin(15))  # DHT22 an GPIO15

# === BMP280 Setup (I2C auf GPIO0 = SDA, GPIO1 = SCL) ===
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)

# print(i2c.scan())  # Überprüft, welche Adressen verfügbar sind - Kann auskommentiert werden, da es nur einmal beim Start kommt
#bmp280_sensor = BMP280(i2c) # This line was missing, assuming it's meant to be here if you have it in your original file

bmp280_sensor = BMP280(i2c) # <--- SICHERSTELLEN, DASS DIESE ZEILE DA IST!

# === UART Setup ===
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

while True:
    dht_temp = None
    dht_hum = None
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
        # print("DHT22 → Temp: {:.1f}°C, Feuchte: {:.1f}%".format(dht_temp, dht_hum)) # <--- DIESE ZEILE AUSKOMMENTIEREN
                                                                                   # Sie sendet Sonderzeichen!
    except Exception as e:
        # print("DHT22 Fehler:", e) # <--- Auch diese Fehler-Ausgaben könnten Sonderzeichen enthalten
        pass # Oder nur loggen, wenn du es nicht am seriellen Monitor sehen musst

    bmp_temp = None
    bmp_press = None
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
        # print("BMP280 → Temp: {:.2f}°C, Druck: {:.2f} hPa".format(bmp_temp, bmp_press)) # <--- DIESE ZEILE AUSKOMMENTIEREN
                                                                                       # Sie sendet Sonderzeichen!
    except Exception as e:
        # print("BMP280 Fehler:", e) # <--- Auch diese Fehler-Ausgaben könnten Sonderzeichen enthalten
        pass # Oder nur loggen

    if uart1.any():
        # Die UART-Kommunikation ist getrennt von der USB-seriellen Ausgabe für den PC-Plot.
        # Diese Zeilen sind okay, solange sie keine Sonderzeichen enthalten
        # die vom PC-Plot-Skript gelesen werden sollen.
        incoming = uart1.read().decode('utf-8').strip()
        print("UART empfangen:", incoming) # Diese Zeile ist OK, da sie für deine UART1-Kommunikation ist
        
        if incoming.lower() == "read":
            try:
                if dht_temp is not None and dht_hum is not None:
                    # Wenn diese Ausgabe nur an UART1 und NICHT an USB geht, ist es okay.
                    # Aber wenn sie auch an den USB-Seriellen geht, kann sie stören.
                    print("Temperatur: {:.1f} °C, Luftfeuchtigkeit: {:.1f} %".format(dht_temp, dht_hum))
                else:
                    dht_sensor.measure()
                    temp_uart = dht_sensor.temperature()
                    hum_uart = dht_sensor.humidity()
                    print("Temperatur: {:.1f} °C, Luftfeuchtigkeit: {:.1f} %".format(temp_uart, hum_uart))
            except OSError as e:
                print("Fehler beim DHT22-Auslesen für UART-Befehl:", e)
        else:
            print("Unbekannter Befehl:", incoming)

    # --- Daten für CSV-Ausgabe (FÜR DEN PLOT!) ---
    current_time = time.time() # Gibt Sekunden seit dem Booten zurück
    
    data_line = "{},{},{},{},{}".format(
        current_time,
        dht_temp if dht_temp is not None else "N/A",
        dht_hum if dht_hum is not None else "N/A",
        bmp_temp if bmp_temp is not None else "N/A",
        bmp_press if bmp_press is not None else "N/A"
    )
    # DIESE IST DIE EINZIGE "print"-AUSGABE, die für das PC-Skript bestimmt ist.
    print(data_line) 

    time.sleep(2)