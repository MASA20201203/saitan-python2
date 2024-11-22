from pathlib import Path
import json

# データを文字列として読み込み、Pythonのオブジェクトに変換する
path = Path('eq_data/eq_data_1_day_m1.geojson')
contents = path.read_text()
all_eq_data = json.loads(contents)

# データセットにある全ての地震を調べる
all_eq_dicts = all_eq_data['features']
print(len(all_eq_dicts))
