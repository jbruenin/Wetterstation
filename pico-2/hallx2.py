from machine import Pin, ADC
import time

# --- Sensor 1 Konfiguration ---
# Digitaler Ausgang (D0) von Sensor 1 an GPIO 15
sensor1_digital_pin = Pin(15, Pin.IN)
# Analoger Ausgang (A0) von Sensor 1 an GPIO 26 (ADC0)
sensor1_analog_pin = ADC(26)

# --- Sensor 2 Konfiguration ---
# Digitaler Ausgang (D0) von Sensor 2 an GPIO 14
sensor2_digital_pin = Pin(14, Pin.IN)
# Analoger Ausgang (A0) von Sensor 2 an GPIO 27 (ADC1)
sensor2_analog_pin = ADC(27)

print("Hall-Sensor-Test gestartet. Halte Magneten an die Sensoren.")
print("Drücke Strg+C in Thonny, um das Programm zu beenden.")

try:
    while True:
        # --- Werte für Sensor 1 auslesen ---
        digital_value_1 = sensor1_digital_pin.value()
        analog_raw_value_1 = sensor1_analog_pin.read_u16()
        analog_voltage_1 = (analog_raw_value_1 / 65535) * 3.3

        # --- Werte für Sensor 2 auslesen ---
        digital_value_2 = sensor2_digital_pin.value()
        analog_raw_value_2 = sensor2_analog_pin.read_u16()
        analog_voltage_2 = (analog_raw_value_2 / 65535) * 3.3

        # --- Ausgabe der Sensorwerte ---
        print(f"Sensor 1: Digital: {'Magnet erkannt!' if digital_value_1 == 0 else 'Kein Magnet'} | Analog (Roh): {analog_raw_value_1} | Analog (Volt): {analog_voltage_1:.2f}V")
        print(f"Sensor 2: Digital: {'Magnet erkannt!' if digital_value_2 == 0 else 'Kein Magnet'} | Analog (Roh): {analog_raw_value_2} | Analog (Volt): {analog_voltage_2:.2f}V")
        print("-" * 50) # Trennlinie für bessere Lesbarkeit

        time.sleep(0.1) # Kurze Pause

except KeyboardInterrupt:
    print("\nProgramm beendet.")