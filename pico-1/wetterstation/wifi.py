import time
import dht
from machine import Pin, I2C
import urequests # Für HTTP-Anfragen
import network   # Für WLAN
import ujson     # Für JSON-Daten

# --- WLAN Konfiguration ---
WIFI_SSID = 'kys'      # <--- ANPASSEN: Dein WLAN-Name
WIFI_PASSWORD = 'kys' # <--- ANPASSEN: Dein WLAN-Passwort

# --- Server Konfiguration auf deinem PC ---
# <--- ANPASSEN: Die IP-Adresse deines Arch Linux PCs
# Finde diese auf deinem PC mit 'ip a' oder 'hostname -I'
PC_SERVER_IP = '192.168.1.100'
PC_SERVER_PORT = 5000
SERVER_URL = f'http://{PC_SERVER_IP}:{PC_SERVER_PORT}/data'

# === DHT22 Setup ===
dht_sensor = dht.DHT22(Pin(15))  # DHT22 an GPIO15

# === BMP280 Setup (I2C auf GPIO0 = SDA, GPIO1 = SCL) ===
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
# print(i2c.scan()) # Kann auskommentiert bleiben
bmp280_sensor = BMP280(i2c)

# --- WLAN-Verbindung herstellen ---
def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    max_attempts = 10
    attempts = 0
    while not wlan.isconnected() and attempts < max_attempts:
        print('Connecting to WLAN...')
        time.sleep(1)
        attempts += 1

    if wlan.isconnected():
        print('WLAN connected! IP:', wlan.ifconfig()[0])
        return True
    else:
        print('Failed to connect to WLAN.')
        return False

# WLAN beim Start verbinden
if not connect_wlan():
    print("WLAN-Verbindung fehlgeschlagen, retrying...")
    # Optional: Reset oder Fallback auf seriellen Modus

while True:
    dht_temp = None
    dht_hum = None
    try:
        dht_sensor.measure()
        dht_temp = dht_sensor.temperature()
        dht_hum = dht_sensor.humidity()
    except Exception as e:
        print("DHT22 Fehler:", e)

    bmp_temp = None
    bmp_press = None
    try:
        bmp_temp = bmp280_sensor.read_temperature()
        bmp_press = bmp280_sensor.read_pressure()
    except Exception as e:
        print("BMP280 Fehler:", e)

    # Daten als Python-Dictionary sammeln
    sensor_data = {
        "timestamp": time.time(), # Nutzt den Pico-Zeitstempel
        "dht_temp": dht_temp,
        "dht_hum": dht_hum,
        "bmp_temp": bmp_temp,
        "bmp_press": bmp_press
    }

    # Daten senden, wenn WLAN verbunden ist
    wlan_status = network.WLAN(network.STA_IF).isconnected()
    if wlan_status:
        try:
            headers = {'Content-Type': 'application/json'}
            response = urequests.post(SERVER_URL, json=sensor_data, headers=headers)
            if response.status_code == 200:
                print(f"Data sent: {sensor_data}")
            else:
                print(f"Failed to send data. Status: {response.status_code}, Response: {response.text}")
            response.close() # Wichtig: Ressourcen freigeben
        except Exception as e:
            print(f"Network request error: {e}")
            # Versuche, WLAN bei Fehler neu zu verbinden
            if not wlan_status:
                connect_wlan()
    else:
        print("WLAN disconnected. Attempting to reconnect...")
        connect_wlan()

    time.sleep(2)