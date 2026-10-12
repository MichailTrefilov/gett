import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.28          # не больше динамического диапазона ЦАП (3.29 В)
signal_frequency = 10
sampling_frequency = 200

if __name__ == "__main__":
    dac = None
    try:
        dac = pwm.PWM_DAC(12, 1000, 3.290)
        start = time.time()

        while True:
            t = time.time() - start
            voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, t)
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)

    except KeyboardInterrupt:
        print("\nГенерация остановлена")

    finally:
        if dac is not None:
            dac.deinit()
