"""
クイックスタート1: 関東一都六県の情報をセットして読み出す
"""
import os
from storekiss.litestore import Client

# データベースファイルのパス
db_path = "quickstart_1.sqlite"

# 既存のファイルがあれば削除
if os.path.exists(db_path):
    os.remove(db_path)

# Firestoreインスタンスを作成
db = Client(db_path)

# 関東一都六県の情報
kanto_prefs = [
    {
        "id": "tokyo",
        "name": "東京都",
        "population": 14047594,
        "area": 2194,
        "capital": "新宿区",
        "established": 1943,
    },
    {
        "id": "kanagawa",
        "name": "神奈川県",
        "population": 9237337,
        "area": 2416,
        "capital": "横浜市",
        "established": 1876,
    },
    {
        "id": "saitama",
        "name": "埼玉県",
        "population": 7344765,
        "area": 3798,
        "capital": "さいたま市",
        "established": 1871,
    },
    {
        "id": "chiba",
        "name": "千葉県",
        "population": 6284480,
        "area": 5158,
        "capital": "千葉市",
        "established": 1873,
    },
    {
        "id": "ibaraki",
        "name": "茨城県",
        "population": 2867009,
        "area": 6097,
        "capital": "水戸市",
        "established": 1875,
    },
    {
        "id": "tochigi",
        "name": "栃木県",
        "population": 1933146,
        "area": 6408,
        "capital": "宇都宮市",
        "established": 1873,
    },
    {
        "id": "gunma",
        "name": "群馬県",
        "population": 1939110,
        "area": 6362,
        "capital": "前橋市",
        "established": 1876,
    },
]

# コレクションの参照を取得
prefectures = db.collection("prefectures")

print("=== 関東一都六県のデータを保存 ===")
# データを保存
for pref in kanto_prefs:
    prefectures.document(pref["id"]).set(pref)
    print(f"{pref['name']}のデータを保存しました")

print("\n=== すべての県のデータを取得 ===")
# すべてのドキュメントを取得
all_prefs = prefectures.get()
for pref in all_prefs:
    print(f"{pref['name']}: 人口 {pref['population']:,}人, 面積 {pref['area']}km²")

print("\n=== 特定の県のデータを取得 ===")
# 特定のドキュメントを取得
tokyo = prefectures.document("tokyo").get()
print(f"ID: {tokyo['id']}")
print(f"名称: {tokyo['name']}")
print(f"人口: {tokyo['population']:,}人")
print(f"面積: {tokyo['area']}km²")
print(f"県庁所在地: {tokyo['capital']}")
print(f"設立年: {tokyo['established']}年")

print("\n=== 人口が500万人以上の県を取得 ===")
# クエリを使用してデータをフィルタリング
large_prefs = [pref for pref in all_prefs if pref["population"] > 5000000]
for pref in large_prefs:
    print(f"{pref['name']}: 人口 {pref['population']:,}人")

print("\n=== 面積が大きい順に並べ替え ===")
# データを並べ替え
sorted_by_area = sorted(all_prefs, key=lambda x: x["area"], reverse=True)
for pref in sorted_by_area:
    print(f"{pref['name']}: 面積 {pref['area']}km²")
