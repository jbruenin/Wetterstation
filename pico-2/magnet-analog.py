from machine import Pin, ADC
import time

# Definiere den GPIO-Pin für den digitalen Ausgang (D0)
hall_sensor_digital_pin = Pin(15, Pin.IN)

# Definiere den GPIO-Pin für den analogen Ausgang (A0)
# GPIO 26 ist ADC0 auf dem Raspberry Pi Pico
hall_sensor_analog_pin = ADC(26)

print("Hall-Sensor-Test gestartet. Halte einen Magneten an den Sensor.")
print("Drücke Strg+C in Thonny, um das Programm zu beenden.")

try:
    while True:
        # Digitalen Wert auslesen
        digital_value = hall_sensor_digital_pin.value()

        # Analogen Wert auslesen
        # Der ADC gibt einen Rohwert zwischen 0 und 65535 (16-Bit) zurück
        analog_raw_value = hall_sensor_analog_pin.read_u16()

        # Konvertiere den Rohwert in eine Spannung (optional, aber hilfreich)
        # Der Pico hat eine 3.3V Referenzspannung für den ADC
        # Spannung = (Rohwert / 65535) * 3.3V
        analog_voltage = (analog_raw_value / 65535) * 3.3

        print(f"Digital: {'Magnet erkannt!' if digital_value == 0 else 'Kein Magnet'} | Analog (Roh): {analog_raw_value} | Analog (Volt): {analog_voltage:.2f}V")

        time.sleep(0.1) # Kurze Pause

except KeyboardInterrupt:
    print("\nProgramm beendet.")