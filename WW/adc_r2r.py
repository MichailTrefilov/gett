import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        self.bits = len(self.bits_gpio)
        self.max_number = 2 ** self.bits - 1  # 255

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        bits = [int(b) for b in bin(number)[2:].zfill(self.bits)]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        for number in range(self.max_number + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)

            comp_value = GPIO.input(self.comp_gpio)
            
            if comp_value == 0:
                return number

        return self.max_number

    def get_sc_voltage(self):
        number = self.sequential_counting_adc()
        voltage = number / self.max_number * self.dynamic_range
        if self.verbose:
            print(f"Число на ЦАП: {number}, напряжение: {voltage:.3f} В")
        return voltage


if __name__ == "__main__":
    adc = None
    try:
        # динамический диапазон нужно предварительно измерить мультиметром
        adc = R2R_ADC(3.3)

        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение: {voltage:.3f} В")

    finally:
        if adc is not None:
            adc.deinit()