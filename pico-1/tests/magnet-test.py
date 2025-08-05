import machine
import utime

# Initialisiere den ADC auf GPIO Pin 26 für das Auslesen des Hall-Sensors.
# Stelle sicher, dass dein Hall-Sensor korrekt an diesen Pin angeschlossen ist.
hall_sensor_adc = machine.ADC(26)

print("Starte Rohdatenanzeige des Hall-Sensors...")
print("Bewege einen Magneten in die Nähe des Sensors, um die Werte zu sehen.")
print("Drücke Strg+C, um die Ausgabe zu stoppen.")

while True:
    # Lese den analogen Wert vom Sensor.
    # Der Wert ist ein 16-Bit-Integer (0-65535).
    value = hall_sensor_adc.read_u16()

    # Gib den gelesenen Wert aus.
    print(f"Aktueller Sensorwert: {value}")

    # Eine kurze Pause, um die CPU nicht zu überlasten und die Ausgabe lesbar zu halten.
    # Du kannst diesen Wert anpassen, um die Abtastrate zu ändern.
    utime.sleep_ms(100)