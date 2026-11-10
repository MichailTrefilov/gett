import time
from smbus2 import SMBus
import matplotlib.pyplot as plt


BUS = 1              
ADDR = 0x48         
FSR = 4.096         
DURATION = 30       
PERIOD = 0.01        

REG_CONV = 0x00
REG_CONFIG = 0x01
CONFIG = 0x42E3      


def read_voltage(bus):
    hi, lo = bus.read_i2c_block_data(ADDR, REG_CONV, 2)
    raw = ((hi << 8) | lo) >> 4
    if raw & 0x800:
        raw -= 1 << 12
    return raw * FSR / 2048


t, v = [], []

with SMBus(BUS) as bus:
    bus.write_i2c_block_data(ADDR, REG_CONFIG, [CONFIG >> 8, CONFIG & 0xFF])
    time.sleep(0.01)

    print(f"Идёт запись {DURATION} с. Нажми кнопку, когда нужно разрядить конденсатор. "
          "Ctrl+C - закончить раньше.")
    t0 = time.time()
    try:
        while time.time() - t0 < DURATION:
            t.append(time.time() - t0)
            v.append(read_voltage(bus))
            time.sleep(PERIOD)
    except KeyboardInterrupt:
        pass

print(f"Записано {len(v)} точек, строю график...")

# максимум напряжения = момент нажатия кнопки: до него заряд, после - разряд
i_max = v.index(max(v))

plt.figure(figsize=(9, 5))
plt.plot(t[:i_max + 1], v[:i_max + 1], "-", label="Заряд")
plt.plot(t[i_max:], v[i_max:], "-", label="Разряд")
plt.axvline(t[i_max], color="gray", linestyle="--", alpha=0.6)
plt.xlabel("Время, с")
plt.ylabel("Напряжение на конденсаторе, В")
plt.title("Заряд и разряд конденсатора")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()