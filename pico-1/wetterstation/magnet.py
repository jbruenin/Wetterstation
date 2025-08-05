import machine
import utime

# Initialisiere den ADC auf GPIO Pin 26 für das Auslesen des Hall-Sensors.
hall_sensor_adc = machine.ADC(26)

# Kalibrierungswerte für die Magneterkennung.
# Diese Werte basieren auf deinen ursprünglichen Schwellenwerten (48000 und 18000).
# Du musst sie möglicherweise feinjustieren, basierend auf den Werten, die du bekommst,
# wenn der Magnet direkt am Sensor vorbeiläuft und wenn er weit entfernt ist.
# Teste, indem du 'print(value)' im Code lässt, während du den Magneten vorbeibewegst.
MAGNET_DETECT_THRESHOLD_HIGH = 48000 # Beispiel: Wert, wenn ein Pol erkannt wird
MAGNET_DETECT_THRESHOLD_LOW = 18000  # Beispiel: Wert, wenn der andere Pol erkannt wird

# Da wir nur einen Magneten haben, der einmal pro Umdrehung vorbeikommt,
# müssen wir uns für EINEN Schwellenwert entscheiden, der eine "Erkennung" markiert.
# Wenn der Magnet einen starken Ausschlag in eine Richtung bewirkt (z.B. sehr hohe Werte),
# nehmen wir diesen als primären Auslöser. Nehmen wir an, es ist der "South pole" Bereich.
# Du kannst auch einen mittleren Schwellenwert nehmen, wenn der Magnet den Wert um einen Ruhezustand ändert.
TRIGGER_THRESHOLD = 20000 # Diesen Wert musst du anpassen!
                             # Er sollte zwischen deinem "Ruhewert" und dem Wert bei Magnetnähe liegen.

# Variablen zur Speicherung der Zeitpunkte und Berechnung der Geschwindigkeit
last_magnet_time = 0
revolutions = 0
wheel_circumference_cm = 200 # Beispiel: Umfang des Rades in cm (z.B. 2 Meter). ANPASSEN!

# Zustand, um Mehrfachzählungen während eines einzigen Magnetvorbeiflugs zu verhindern
magnet_currently_detected = False

print("Starte Geschwindigkeitsmessung (ADC-Modus)...")
print(f"Radumfang eingestellt auf: {wheel_circumference_cm} cm")
print(f"Trigger-Schwellenwert eingestellt auf: {TRIGGER_THRESHOLD}")

while True:
    # Lese den analogen Wert vom Sensor
    value = hall_sensor_adc.read_u16()

    # Optional: Ausgabe des Rohwerts zur Kalibrierung/Fehlersuche
    # Kommentiere dies aus, sobald du die Schwellenwerte eingestellt hast.
    # print(f"Aktueller Sensorwert: {value}")

    # Logik zur Erkennung eines einzelnen Ereignisses pro Umdrehung
    # Wir suchen nach einem Übergang: Wert übersteigt den Schwellenwert
    # UND wir haben den Magneten vorher nicht als "aktuell erkannt" markiert.
    if value >= TRIGGER_THRESHOLD and not magnet_currently_detected:
        # Magnet wurde gerade erkannt
        current_time = utime.ticks_ms()
        time_since_last_magnet = utime.ticks_diff(current_time, last_magnet_time)

        # Entprellung (Software): Ignoriere sehr schnelle aufeinanderfolgende Erkennungen.
        # Dieser Wert muss >0 sein und sollte größer sein als die Zeit, die der Magnet braucht,
        # um am Sensor vorbeizukommen, aber kleiner als die Zeit für eine halbe Umdrehung.
        # Da du 140ms als typische Zeit hattest, ist 100ms ein guter Startpunkt.
        DEBOUNCE_TIME_MS = 100

        if time_since_last_magnet > DEBOUNCE_TIME_MS:
            revolutions += 1
            last_magnet_time = current_time

            # Berechne die Geschwindigkeit
            if time_since_last_magnet > 0: # Division durch Null vermeiden
                speed_cm_per_sec = wheel_circumference_cm / (time_since_last_magnet / 1000)
                speed_km_per_hour = speed_cm_per_sec * 0.036
                print(f"Umdrehung: {revolutions}, Zeit seit letztem Magnet: {time_since_last_magnet} ms, Geschwindigkeit: {speed_km_per_hour:.2f} km/h")

            # Setze den Status, dass der Magnet derzeit erkannt wird, um Mehrfachzählungen zu verhindern
            magnet_currently_detected = True

    # Wenn der Wert unter den Schwellenwert fällt UND der Magnet zuvor als erkannt markiert war,
    # setzen wir den Zustand zurück, damit der Sensor für die nächste Umdrehung wieder zählen kann.
    # Dieser "Reset-Schwellenwert" kann etwas niedriger sein, um Hysterese zu schaffen.
    # Verwende hier einen Wert, der eindeutig unter dem Trigger-Schwellenwert liegt,
    # aber immer noch über dem "Kein-Magnet"-Wert.
    elif value < (TRIGGER_THRESHOLD - 5000) and magnet_currently_detected: # Beispiel: 5000 niedriger
        magnet_currently_detected = False

    # Eine kurze Pause, um die CPU nicht zu überlasten und stabile Messwerte zu erhalten.
    # Dieser Wert beeinflusst die "Abtastrate". Je kleiner, desto genauer die Erkennung,
    # aber desto höher die CPU-Last. 10ms ist ein guter Kompromiss.
    utime.sleep_ms(10)