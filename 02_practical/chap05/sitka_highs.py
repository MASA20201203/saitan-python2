from pathlib import Path
import csv

import matplotlib.pyplot as plt

path = Path('weather_data/sitka_weather_07-2021_simple.csv')
lines = path.read_text().splitlines()

render = csv.reader(lines)
header_row = next(render)

# 最高気温を取り出す
highs = []
for row in render:
    high = int(row[4])
    highs.append(high)

# 最高気温のグラフを描画する
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(highs, c='red')

# グラフのフォーマット設定
plt.title('Daily high temperatures, July 2021', fontsize=24)
plt.xlabel('', fontsize=16)
plt.ylabel('Temperature (F)', fontsize=16)
plt.tick_params(labelsize=16)

plt.show()
