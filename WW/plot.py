import csv
import matplotlib.pyplot as plt
 
FILE = "data_i2c.csv"
 
t, v = [], []
with open(FILE) as f:
    for row in csv.DictReader(f):
        t.append(float(row["time"]))
        v.append(float(row["voltage"]))
 
# момент нажатия кнопки = максимум напряжения: до него заряд, после - разряд
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
plt.savefig("graph_i2c.png", dpi=150)
plt.show()