import os
import json
import datetime
from storekiss.crud import LiteStore
# from storekiss.validation import Schema, StringField, NumberField, BooleanField
from storekiss.export_import import LiteStoreExporter, LiteStoreImporter

# tests/temp_test_data ディレクトリにテスト用のディレクトリを生成
os.makedirs("tests/temp_test_data", exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
export_dir = os.path.join("tests/temp_test_data", f"test_export_fix_{timestamp}")
os.makedirs(export_dir, exist_ok=True)

# tests/temp_test_data ディレクトリにテスト用のデータベースファイルを生成
db_path = os.path.join("tests/temp_test_data", f"test_export_fix_{timestamp}.sqlite")
if os.path.exists(db_path):
    os.remove(db_path)

# LiteStoreインスタンスを作成
db = LiteStore(db_path=db_path)

# 都道府県コレクションを作成
prefectures = db.collection("prefectures")

# いくつかの都道府県データを追加
prefectures.document("hokkaido").set({"number": 1, "name": "北海道", "active": True})

# データベースから直接データを取得して確認
print("=== データベースから直接取得したデータ ===")
docs = prefectures.get()
for doc in docs:
    doc_data = doc.to_dict()
    print(
        f"  {doc.id}: {doc_data['name']} (active: {doc_data['active']}, 型: {type(doc_data['active'])})"
    )

# エクスポーターを直接使用してデータを変換
print("\n=== エクスポーターでの変換テスト ===")
exporter = LiteStoreExporter(db)
doc_data = {"number": 1, "name": "北海道", "active": True}
litestore_fields = exporter._convert_to_litestore_fields(doc_data)
print(f"変換後のフィールド: {json.dumps(litestore_fields, indent=2)}")

# エクスポートファイルを作成
print("\n=== エクスポート ===")
metadata_file = exporter.export_collection("prefectures", export_dir)
print(f"メタデータファイル: {metadata_file}")

# エクスポートされたJSONLファイルの内容を確認
jsonl_file = os.path.join(export_dir, "prefectures", "prefectures.jsonl")
print(f"\nエクスポートされたJSONLファイルの内容:")
with open(jsonl_file, "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)
        print(f"  ドキュメントID: {doc['name'].split('/')[-1]}")
        print(f"  フィールド: {json.dumps(doc['fields'], indent=2)}")

# インポーターを直接使用してデータを変換
print("\n=== インポーターでの変換テスト ===")
importer = LiteStoreImporter(db)
test_fields = {
    "number": {"integerValue": "1"},
    "name": {"stringValue": "北海道"},
    "active": {"integerValue": "True"},  # 問題のあるフィールド
}
try:
    converted_data = importer._convert_from_litestore_fields(test_fields)
    print(f"変換後のデータ: {converted_data}")
except Exception as e:
    print(f"変換エラー: {e}")

# 修正版の変換メソッドを実装
def fixed_convert_from_litestore_fields(fields):
    """修正版のLiteStoreフィールド変換メソッド"""
    result = {}
    for key, value_container in fields.items():
        value_type, value = next(iter(value_container.items()))

        if value_type == "stringValue":
            result[key] = value
        elif value_type == "integerValue":
            # ブール値の文字列が整数として保存されている場合の処理
            if value == "True":
                result[key] = True
            elif value == "False":
                result[key] = False
            else:
                result[key] = int(value)
        elif value_type == "doubleValue":
            result[key] = float(value)
        elif value_type == "booleanValue":
            if isinstance(value, str):
                result[key] = value.lower() == "true"
            else:
                result[key] = bool(value)
        elif value_type == "nullValue":
            result[key] = None
        else:
            result[key] = str(value)

    return result


# 修正版の変換メソッドでテスト
print("\n=== 修正版変換メソッドでのテスト ===")
try:
    fixed_data = fixed_convert_from_litestore_fields(test_fields)
    print(f"修正版変換後のデータ: {fixed_data}")
except Exception as e:
    print(f"修正版変換エラー: {e}")
