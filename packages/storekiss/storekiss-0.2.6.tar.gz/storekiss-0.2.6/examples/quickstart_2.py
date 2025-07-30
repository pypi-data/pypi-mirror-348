"""
クイックスタート2: サブコレクションを使用して各都道府県の都市情報を管理する
"""
import os
from storekiss.litestore import Client

# データベースファイルのパス
db_path = "quickstart_2.sqlite"

# 既存のファイルがあれば削除
if os.path.exists(db_path):
    os.remove(db_path)

# Firestoreインスタンスを作成
db = Client(db_path)

# 関東一都六県の情報
kanto_prefs = [
    {"id": "tokyo", "name": "東京都", "population": 14047594, "area": 2194},
    {"id": "kanagawa", "name": "神奈川県", "population": 9237337, "area": 2416},
    {"id": "saitama", "name": "埼玉県", "population": 7344765, "area": 3798},
    {"id": "chiba", "name": "千葉県", "population": 6284480, "area": 5158},
    {"id": "ibaraki", "name": "茨城県", "population": 2867009, "area": 6097},
    {"id": "tochigi", "name": "栃木県", "population": 1933146, "area": 6408},
    {"id": "gunma", "name": "群馬県", "population": 1939110, "area": 6362},
]

# 都市情報
cities_data = {
    "tokyo": [
        {
            "id": "shinjuku",
            "name": "新宿区",
            "population": 346235,
            "is_special_ward": True,
        },
        {"id": "shibuya", "name": "渋谷区", "population": 228906, "is_special_ward": True},
        {"id": "minato", "name": "港区", "population": 258875, "is_special_ward": True},
        {
            "id": "hachioji",
            "name": "八王子市",
            "population": 577513,
            "is_special_ward": False,
        },
    ],
    "kanagawa": [
        {
            "id": "yokohama",
            "name": "横浜市",
            "population": 3757630,
            "is_designated_city": True,
        },
        {
            "id": "kawasaki",
            "name": "川崎市",
            "population": 1539522,
            "is_designated_city": True,
        },
        {
            "id": "sagamihara",
            "name": "相模原市",
            "population": 720780,
            "is_designated_city": True,
        },
    ],
    "saitama": [
        {
            "id": "saitama_city",
            "name": "さいたま市",
            "population": 1324025,
            "is_designated_city": True,
        },
        {
            "id": "kawagoe",
            "name": "川越市",
            "population": 350745,
            "is_designated_city": False,
        },
        {
            "id": "kawaguchi",
            "name": "川口市",
            "population": 592377,
            "is_designated_city": False,
        },
    ],
    "chiba": [
        {
            "id": "chiba_city",
            "name": "千葉市",
            "population": 971882,
            "is_designated_city": True,
        },
        {
            "id": "funabashi",
            "name": "船橋市",
            "population": 641114,
            "is_designated_city": False,
        },
        {
            "id": "matsudo",
            "name": "松戸市",
            "population": 495344,
            "is_designated_city": False,
        },
    ],
    "ibaraki": [
        {"id": "mito", "name": "水戸市", "population": 269103, "is_core_city": True},
        {"id": "tsukuba", "name": "つくば市", "population": 243735, "is_core_city": False},
        {"id": "hitachi", "name": "日立市", "population": 169178, "is_core_city": False},
    ],
    "tochigi": [
        {
            "id": "utsunomiya",
            "name": "宇都宮市",
            "population": 518665,
            "is_core_city": True,
        },
        {"id": "ashikaga", "name": "足利市", "population": 146927, "is_core_city": False},
        {
            "id": "tochigi_city",
            "name": "栃木市",
            "population": 156351,
            "is_core_city": False,
        },
    ],
    "gunma": [
        {"id": "maebashi", "name": "前橋市", "population": 331576, "is_core_city": True},
        {"id": "takasaki", "name": "高崎市", "population": 370884, "is_core_city": True},
        {"id": "ota", "name": "太田市", "population": 219807, "is_core_city": False},
    ],
}

# コレクションの参照を取得
prefectures = db.collection("prefectures")

print("=== 関東一都六県のデータを保存 ===")
# 都道府県データを保存
for pref in kanto_prefs:
    prefectures.document(pref["id"]).set(pref)
    print(f"{pref['name']}のデータを保存しました")

print("\n=== 各都道府県の都市データをサブコレクションに保存 ===")
# 各都道府県の都市データを別のコレクションに保存
# 都市コレクションを作成
cities = db.collection("cities")

for pref_id, city_list in cities_data.items():
    # 都道府県の情報を取得
    pref_name = next(p["name"] for p in kanto_prefs if p["id"] == pref_id)

    # 都市データを保存
    for city in city_list:
        # 都市ドキュメントIDを作成（都道府県のIDを含める）
        city_doc_id = f"{pref_id}_{city['id']}"

        # 都道府県情報を都市データに追加
        city_data = city.copy()
        city_data["prefecture_id"] = pref_id
        city_data["prefecture_name"] = pref_name

        # 都市データを保存
        cities.document(city_doc_id).set(city_data)
        print(f"{pref_name}の{city['name']}のデータを保存しました")

print("\n=== 各都道府県の都市データを取得して表示 ===")
# すべての都道府県を取得
all_prefs = prefectures.get()

# 都市コレクションを取得
cities_collection = db.collection("cities")
all_cities = cities_collection.get()

# 各都道府県の都市データを表示
for pref in all_prefs:
    print(f"\n【{pref['name']}の都市】")

    # この都道府県に属する都市をフィルタリング
    pref_cities = [
        city for city in all_cities if city.get("prefecture_id") == pref["id"]
    ]

    # 都市データを表示
    for city in pref_cities:
        print(f"  {city['name']}: 人口 {city['population']:,}人")

print("\n=== 特定の都道府県（東京都）の都市データのみを取得 ===")
# 都市コレクションから東京都の都市だけをフィルタリング
tokyo_cities = [city for city in all_cities if city.get("prefecture_id") == "tokyo"]

# 東京都の都市データを表示
print(f"東京都の都市数: {len(tokyo_cities)}")
for city in tokyo_cities:
    special_ward_text = "特別区" if city.get("is_special_ward", False) else "市"
    print(f"  {city['name']}（{special_ward_text}）: 人口 {city['population']:,}人")

print("\n=== 人口50万人以上の都市を持つ都道府県を表示 ===")
# すべての都道府県を取得
for pref in all_prefs:
    # この都道府県に属する都市をフィルタリング
    pref_cities = [
        city for city in all_cities if city.get("prefecture_id") == pref["id"]
    ]

    # 人口50万人以上の都市をフィルタリング
    large_cities = [city for city in pref_cities if city["population"] > 500000]

    if large_cities:
        print(f"\n【{pref['name']}の人口50万人以上の都市】")
        for city in large_cities:
            print(f"  {city['name']}: 人口 {city['population']:,}人")
