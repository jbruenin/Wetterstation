# bmp280.py
import time
import struct

class BMP280:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        self.dig_T = []
        self.dig_P = []
        self.t_fine = 0
        self._load_calibration()
        self._configure()

    def _load_calibration(self):
        calib = self.i2c.readfrom_mem(self.addr, 0x88, 24)
        self.dig_T = list(struct.unpack('<Hhh', calib[0:6]))
        self.dig_P = list(struct.unpack('<Hhhhhhhhh', calib[6:24]))

    def _configure(self):
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x27')  # Normal mode, temp & press oversampling x1
        self.i2c.writeto_mem(self.addr, 0xF5, b'\xA0')  # Standby 1000ms

    def read_raw_data(self):
        data = self.i2c.readfrom_mem(self.addr, 0xF7, 6)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        return adc_t, adc_p

    def read_temperature(self):
        adc_t, _ = self.read_raw_data()
        var1 = (((adc_t >> 3) - (self.dig_T[0] << 1)) * self.dig_T[1]) >> 11
        var2 = (((((adc_t >> 4) - self.dig_T[0]) * ((adc_t >> 4) - self.dig_T[0])) >> 12) * self.dig_T[2]) >> 14
        self.t_fine = var1 + var2
        temp = (self.t_fine * 5 + 128) >> 8
        return temp / 100.0

    def read_pressure(self):
        _, adc_p = self.read_raw_data()
        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P[5]
        var2 = var2 + ((var1 * self.dig_P[4]) << 17)
        var2 = var2 + (self.dig_P[3] << 35)
        var1 = ((var1 * var1 * self.dig_P[2]) >> 8) + ((var1 * self.dig_P[1]) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P[0]) >> 33
        if var1 == 0:
            return 0
        p = 1048576 - adc_p
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (self.dig_P[8] * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P[7] * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.dig_P[6] << 4)
        return p / 25600.0