import time
import RPi.GPIO as GPIO
from mcp3021_driver import MCP3021
 
# ---------- Настройки ----------
SIG = 14              # пин, к которому подключена плата (заряд конденсатора)
DYNAMIC_RANGE = 3.3   # опорное напряжение АЦП, В
ADDRESS = 0x4D        # адрес АЦП, проверь: i2cdetect -y 1
DURATION = 30         # сколько секунд записывать
PERIOD = 0.01         # пауза между измерениями, с
OUT_FILE = "data_i2c.csv"
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SIG, GPIO.OUT, initial=GPIO.LOW)
 
adc = None
data = []
 
try:
    adc = MCP3021(DYNAMIC_RANGE, ADDRESS, verbose=False)
 
    # на gpio14 высокий уровень - конденсатор заряжается
    GPIO.output(SIG, GPIO.HIGH)
 
    print(f"Идёт запись {DURATION} с. Дай конденсатору зарядиться, "
          "потом нажми кнопку на плате - он разрядится. Ctrl+C - закончить раньше.")
    t0 = time.time()
 
    while time.time() - t0 < DURATION:
        data.append((time.time() - t0, adc.get_voltage()))
        time.sleep(PERIOD)
 
except KeyboardInterrupt:
    pass
 
finally:
    GPIO.output(SIG, GPIO.LOW)
    GPIO.cleanup()
    if adc is not None:
        adc.deinit()
 
with open(OUT_FILE, "w") as f:
    f.write("time,voltage\n")
    for t, v in data:
        f.write(f"{t:.5f},{v:.4f}\n")
 
print(f"Готово: {len(data)} точек сохранено в {OUT_FILE}")