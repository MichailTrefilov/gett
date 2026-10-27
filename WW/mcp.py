import time

from mcp3021_driver import MCP3021
import adc_plot

# динамический диапазон: измерьте мультиметром напряжение на контакте PWR
# блока AUX при перемычке на 5V (значение ниже примерное)
dynamic_range = 5.0

mcp = MCP3021(dynamic_range)

voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()

    while time.time() - start_time < duration:
        voltage_values.append(mcp.get_voltage())
        time_values.append(time.time() - start_time)

    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

finally:
    mcp.deinit()