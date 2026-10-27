import time

from r2r_adc import R2R_ADC
import adc_plot

# динамический диапазон нужно предварительно измерить мультиметром
dynamic_range = 3.3

adc = R2R_ADC(dynamic_range, compare_time=0.0005)

voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()

    while time.time() - start_time < duration:
        voltage_values.append(adc.get_sar_voltage())
        time_values.append(time.time() - start_time)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)
    adc_plot.plot_sampling_period_hist(time_values)

finally:
    adc.deinit()