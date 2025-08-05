class HM3301:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address

    def read_data(self):
        try:
            data = self.i2c.readfrom(self.address, 29)
        except Exception as e:
            raise RuntimeError("I2C-Lesefehler: {}".format(e))

        # Prüfe Header (Byte 0 und 1)
        if data[0] != 0x88 or data[1] != 0x66:
            raise ValueError("Ungültiger Header: 0x{:02X} 0x{:02X}".format(data[0], data[1]))

        # Prüfe Länge (Byte 2 = 0x00, Byte 3 = 0x1D)
        if data[2] != 0x00 or data[3] != 0x1D:
            raise ValueError("Ungültige Datenlänge")

        # Prüfe Checksumme (Summe Byte 0–27 & 0xFF = Byte 28)
        checksum = sum(data[0:28]) & 0xFF
        if checksum != data[28]:
            raise ValueError("Ungültige Prüfsumme")

        # Extrahiere Partikelkonzentrationen
        pm1_0 = (data[4] << 8) | data[5]
        pm2_5 = (data[6] << 8) | data[7]
        pm10  = (data[8] << 8) | data[9]

        return {
            "PM1.0": pm1_0,
            "PM2.5": pm2_5,
            "PM10": pm10
        }
