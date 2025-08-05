from machine import I2C, Pin
import time

# I2C Setup: GP0 -> SDA, GP1 -> SCL
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Adresse des HM3301 (0x40)
HM3301_ADDR = 0x40

# Funktion zum Auslesen der Feinstaubdaten
def read_hm3301():
    try:
        # Lese 32 Bytes vom HM3301 (ab Adresse 0x00)
        data = i2c.readfrom(HM3301_ADDR, 32)
        
        # PM2.5 und PM10 aus den entsprechenden Bytes extrahieren
        pm25 = (data[4] << 8) | data[5]
        pm10 = (data[6] << 8) | data[7]
        
        print(f"PM2.5: {pm25} µg/m³")
        print(f"PM10: {pm10} µg/m³")

    except Exception as e:
        print("Fehler beim Auslesen des HM3301:", e)

# Feinstaubwerte auslesen
read_hm3301()
