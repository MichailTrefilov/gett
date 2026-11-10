import smbus
import time
 
 
class MCP3021:
    def __init__(self, dynamic_range, address=0x4D, verbose=True):
        self.bus = smbus.SMBus(1)
 
        self.address = address
        self.verbose = verbose
        self.dynamic_range = dynamic_range
 
    def deinit(self):
        self.bus.close()
 
    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
 
        # smbus отдаёт слово с переставленными байтами
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
 
        # формат MCP3021: 4 нуля, 10 бит данных, 2 нуля
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
 
        if self.verbose:
            print(f"Принятые по I2C данные: 0x{upper_data_byte:02X} 0x{lower_data_byte:02X}, "
                  f"число: {number}")
 
        return number
 
    def get_voltage(self):
        number = self.get_number()
        return number / 1023 * self.dynamic_range
 
 
if __name__ == "__main__":
    adc = None
    try:
        adc = MCP3021(3.3, 0x4D)
 
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В\n")
            time.sleep(0.5)
 
    finally:
        if adc is not None:
            adc.deinit()
 