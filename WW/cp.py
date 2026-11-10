import time
from smbus2 import SMBus
 
# ---------- Настройки ----------
BUS = 1              # I2C шина (пины gpio2 SDA / gpio3 SCL = шина 1)
ADDR = 0x48          # адрес АЦП, проверь командой: i2cdetect -y 1
FSR = 4.096          # диапазон АЦП, В (должен покрывать напряжение на конденсаторе)
DURATION = 30        # сколько секунд записывать
PERIOD = 0.01        # пауза между измерениями, с
OUT_FILE = "data_i2c.csv"
 
REG_CONV = 0x00
REG_CONFIG = 0x01
# AIN0 vs GND, ±4.096 В, непрерывный режим, 3300 SPS, компаратор выключен
CONFIG = 0x42E3
 
 
def init(bus):
    bus.write_i2c_block_data(ADDR, REG_CONFIG, [CONFIG >> 8, CONFIG & 0xFF])
    time.sleep(0.01)
 
 
def read_voltage(bus):
    hi, lo = bus.read_i2c_block_data(ADDR, REG_CONV, 2)
    raw = ((hi << 8) | lo) >> 4          # 12 бит
    if raw & 0x800:                      # знак
        raw -= 1 << 12
    return raw * FSR / 2048
 
 
with SMBus(BUS) as bus:
    init(bus)
    data = []
    print(f"Запись {DURATION} с... Нажми кнопку на плате, когда нужно разрядить конденсатор. "
          "Ctrl+C - остановить раньше.")
    t0 = time.time()
    try:
        while time.time() - t0 < DURATION:
            t = time.time() - t0
            data.append((t, read_voltage(bus)))
            time.sleep(PERIOD)
    except KeyboardInterrupt:
        pass
 
with open(OUT_FILE, "w") as f:
    f.write("time,voltage\n")
    for t, v in data:
        f.write(f"{t:.5f},{v:.4f}\n")
 
print(f"Готово: {len(data)} точек сохранено в {OUT_FILE}")
 