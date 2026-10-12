import mcp4725_driver as mcp
import signal_generator as sg
import time

amplitude = 5.0           # не больше динамического диапазона ЦАП (5.11 В)
signal_frequency = 10
sampling_frequency = 1000

if __name__ == "__main__":
    dac = None
    try:
        dac = mcp.MCP4725(5.11, 0x61, verbose=False)
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
