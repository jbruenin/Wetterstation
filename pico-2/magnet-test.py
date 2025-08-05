from machine import Pin
import time

# Definiere den GPIO-Pin, an den der D0-Ausgang des Sensors angeschlossen ist
# Wir verwenden GPIO 15 (GP15) als Beispiel
hall_sensor_pin = Pin(15, Pin.IN)

print("Hall-Sensor-Test gestartet. Halte einen Magneten an den Sensor.")
print("Drücke Strg+C in Thonny, um das Programm zu beenden.")

try:
    while True:
        # Lese den Zustand des Pins aus
        # Der A3144 hat normalerweise einen Open-Collector-Ausgang
        # und das Modul hat oft einen Pull-up Widerstand.
        # Bei Annäherung eines Magnetfeldes schaltet der Ausgang auf LOW.
        # Daher ist 0 (False) = Magnetfeld erkannt, 1 (True) = kein Magnetfeld.
        if hall_sensor_pin.value() == 0:
            print("Magnetfeld erkannt!")
        else:
            # print("Kein Magnetfeld.") # Auskommentiert, damit die Ausgabe nicht überflutet wird
            pass

        time.sleep(0.1) # Kurze Pause, um die CPU nicht zu überlasten

except KeyboardInterrupt:
    print("\nProgramm beendet.")