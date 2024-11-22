from pathlib import Path
import csv

path = Path('weather_data/sitka_weather_07-2021_simple.csv')
lines = path.read_text().splitlines()

render = csv.reader(lines)
header_row = next(render)
print(header_row)
