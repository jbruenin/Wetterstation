import time
import dht
from machine import Pin, UART

# DHT11 Setup (Datenleitung an z. B. GPIO15)
dht_sensor = dht.DHT11(Pin(15))

# UART Setup (UART1, TX=GPIO4, RX=GPIO5)
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Loop
while True:
    # DHT11 auslesen
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print("DHT11 → Temp: {}°C, Feuchte: {}%".format(temp, hum))
    except Exception as e:
        print("DHT11 Fehler:", e)

    # UART-Daten auslesen (falls vorhanden)
    if uart.any():
        uart_data = uart.readline()
        if uart_data:
            print("UART →", uart_data.decode('utf-8').strip())

    time.sleep(2)