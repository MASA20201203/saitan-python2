from pathlib import Path
import csv

path = Path('weather_data/sitka_weather_07-2021_simple.csv')
lines = path.read_text().splitlines()

render = csv.reader(lines)
header_row = next(render)

# 最高気温を取り出す
highs = []
for row in render:
    high = int(row[4])
    highs.append(high)

print(highs)
