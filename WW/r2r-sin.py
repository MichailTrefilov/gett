import r2r_dac as r2r
import signal_generator as sg
import time

amplitude = 3.18          # не больше динамического диапазона ЦАП (3.183 В)
signal_frequency = 10
sampling_frequency = 1000

if __name__ == "__main__":
    dac = None
    try:
        dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183)
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
