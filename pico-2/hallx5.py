from machine import Pin, ADC
import time

# --- Sensor 1 Konfiguration ---
sensor1_digital_pin = Pin(15, Pin.IN) # D0 an GP15
sensor1_analog_pin = ADC(26)         # A0 an GP26 (ADC0)

# --- Sensor 2 Konfiguration ---
sensor2_digital_pin = Pin(14, Pin.IN) # D0 an GP14
sensor2_analog_pin = ADC(27)         # A0 an GP27 (ADC1)

# --- Sensor 3 Konfiguration ---
sensor3_digital_pin = Pin(13, Pin.IN) # D0 an GP13
sensor3_analog_pin = ADC(28)         # A0 an GP28 (ADC2)

# --- Sensor 4 Konfiguration (nur digital) ---
sensor4_digital_pin = Pin(12, Pin.IN) # D0 an GP12
# Sensor 4 A0 kann nicht analog gelesen werden (keine ADC-Pins mehr frei)

# --- Sensor 5 Konfiguration (nur digital) ---
sensor5_digital_pin = Pin(11, Pin.IN) # D0 an GP11
# Sensor 5 A0 kann nicht analog gelesen werden (keine ADC-Pins mehr frei)


print("Hall-Sensor-Test für 5 Sensoren gestartet.")
print("Hinweis: Nur Sensor 1, 2 und 3 können analog ausgelesen werden.")
print("Drücke Strg+C in Thonny, um das Programm zu beenden.")

try:
    while True:
        # --- Werte für Sensor 1 auslesen ---
        digital_value_1 = sensor1_digital_pin.value()
        analog_raw_value_1 = sensor1_analog_pin.read_u16()
        analog_voltage_1 = (analog_raw_value_1 / 65535) * 3.3
        print(f"S1: Digital: {'Magnet!' if digital_value_1 == 0 else 'Kein Magnet'} | Analog: {analog_raw_value_1} ({analog_voltage_1:.2f}V)")

        # --- Werte für Sensor 2 auslesen ---
        digital_value_2 = sensor2_digital_pin.value()
        analog_raw_value_2 = sensor2_analog_pin.read_u16()
        analog_voltage_2 = (analog_raw_value_2 / 65535) * 3.3
        print(f"S2: Digital: {'Magnet!' if digital_value_2 == 0 else 'Kein Magnet'} | Analog: {analog_raw_value_2} ({analog_voltage_2:.2f}V)")

        # --- Werte für Sensor 3 auslesen ---
        digital_value_3 = sensor3_digital_pin.value()
        analog_raw_value_3 = sensor3_analog_pin.read_u16()
        analog_voltage_3 = (analog_raw_value_3 / 65535) * 3.3
        print(f"S3: Digital: {'Magnet!' if digital_value_3 == 0 else 'Kein Magnet'} | Analog: {analog_raw_value_3} ({analog_voltage_3:.2f}V)")

        # --- Werte für Sensor 4 auslesen (nur digital) ---
        digital_value_4 = sensor4_digital_pin.value()
        print(f"S4: Digital: {'Magnet!' if digital_value_4 == 0 else 'Kein Magnet'} | Analog: Nicht verfügbar (kein ADC-Pin)")

        # --- Werte für Sensor 5 auslesen (nur digital) ---
        digital_value_5 = sensor5_digital_pin.value()
        print(f"S5: Digital: {'Magnet!' if digital_value_5 == 0 else 'Kein Magnet'} | Analog: Nicht verfügbar (kein ADC-Pin)")

        print("-" * 60) # Trennlinie für bessere Lesbarkeit

        time.sleep(0.1) # Kurze Pause

except KeyboardInterrupt:
    print("\nProgramm beendet.")