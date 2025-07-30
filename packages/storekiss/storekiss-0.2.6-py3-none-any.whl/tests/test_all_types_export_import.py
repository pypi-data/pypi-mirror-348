import os
import json
import datetime
from storekiss.crud import LiteStore
# from storekiss.validation import (
#     StringField,
#     NumberField,
#     BooleanField,
#     MapField,
#     ListField,
#     DateTimeField,
# )

# tests/temp_test_data ディレクトリにテスト用のディレクトリを生成
os.makedirs("tests/temp_test_data", exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
export_dir = os.path.join("tests/temp_test_data", f"test_all_types_export_{timestamp}")
os.makedirs(export_dir, exist_ok=True)

# tests/temp_test_data ディレクトリにテスト用のデータベースファイルを生成
db_path = os.path.join("tests/temp_test_data", f"test_all_types_{timestamp}.sqlite")
if os.path.exists(db_path):
    os.remove(db_path)

# すべての型を含むスキーマを定義
# all_types_schema = Schema(
#     fields={
#         "string_field": StringField(required=True),
#         "number_field": NumberField(required=True),
#         "boolean_field": BooleanField(required=True),
#         "map_field": MapField(
#             field_validators={
#                 "nested_string": StringField(required=False),
#                 "nested_number": NumberField(required=False),
#                 "nested_boolean": BooleanField(required=False),
#             },
#             required=False,
#             # allow_extra_fields=True,
#         ),
#         # カスタムバリデーターを作成して、あらゆる型を許容する
#         "array_field": ListField(
#             item_validator=FieldValidator(required=False), required=False
#         ),
#     }
# )

# LiteStoreインスタンスを作成
db = LiteStore(db_path=db_path)

# すべての型を含むコレクションを作成
all_types = db.collection("all_types")  

# 現在時刻を取得
now = datetime.datetime.now()

# すべての型を含むドキュメントを追加
all_types.document("doc1").set(
    {
        "string_field": "テスト文字列",
        "number_field": 123,
        "boolean_field": True,
        "map_field": {
            "nested_string": "ネストされた文字列",
            "nested_number": 456,
            "nested_boolean": False,
            "nested_map": {"double_nested": "二重ネスト"},
        },
        "array_field": ["配列の文字列", 789, True, {"array_map": "配列内のマップ"}, [1, 2, 3]],
        "timestamp_field": now,
        "null_field": None,
    }
)

# 浮動小数点数を含むドキュメントを追加
all_types.document("doc2").set(
    {
        "string_field": "浮動小数点数テスト",
        "number_field": 123.456,
        "boolean_field": False,
        "array_field": [1.23, 4.56, 7.89],
    }
)

# データベースから直接データを取得して確認
print("=== データベースから直接取得したデータ ===")
docs = all_types.get()
for doc in docs:
    print(f"ドキュメントID: {doc.id}")
    doc_data = doc.to_dict()
    for key, value in doc_data.items():
        print(f"  {key}: {value} (型: {type(value).__name__})")
    print()

# コレクションをエクスポート
print("\n=== エクスポート ===")
metadata_file = db.export_collection("all_types", export_dir)
print(f"メタデータファイル: {metadata_file}")

# メタデータファイルの内容を確認
with open(metadata_file, "r", encoding="utf-8") as f:
    metadata = json.load(f)
    print(f"バージョン: {metadata['version']}")
    print(f"エクスポート時間: {metadata['exportTime']}")
    print(f"コレクション数: {len(metadata['collections'])}")
    print(f"ドキュメント数: {metadata['collections'][0]['documentCount']}")

# エクスポートされたJSONLファイルの内容を確認
jsonl_file = os.path.join(export_dir, "all_types", "all_types.jsonl")
print(f"\nエクスポートされたJSONLファイルの内容:")
with open(jsonl_file, "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)
        print(f"ドキュメントID: {doc['name'].split('/')[-1]}")
        print(f"フィールド型:")
        for field_name, field_value in doc["fields"].items():
            field_type = list(field_value.keys())[0]
            print(f"  {field_name}: {field_type}")
        print()

# 新しいデータベースを作成してインポート
print("\n=== インポート ===")
new_db_path = os.path.join(
    "tests/temp_test_data", f"test_all_types_import_{timestamp}.sqlite"
)
if os.path.exists(new_db_path):
    os.remove(new_db_path)

new_db = LiteStore(db_path=new_db_path)  
imported_count = new_db.import_collection("all_types", export_dir)
print(f"インポートされたドキュメント数: {imported_count}")

# インポートされたデータを確認
imported_all_types = new_db.collection("all_types")
print("\nインポートされたデータ:")
imported_docs = imported_all_types.get()
for doc in imported_docs:
    print(f"ドキュメントID: {doc.id}")
    doc_data = doc.to_dict()
    for key, value in doc_data.items():
        print(f"  {key}: {value} (型: {type(value).__name__})")
    print()

# 元のデータとインポートされたデータの比較
print("\n=== データ比較 ===")
original_docs = {doc.id: doc.to_dict() for doc in docs}
imported_docs_dict = {doc.id: doc.to_dict() for doc in imported_docs}

for doc_id, original_doc in original_docs.items():
    if doc_id in imported_docs_dict:
        imported_doc = imported_docs_dict[doc_id]
        print(f"ドキュメントID: {doc_id}")

        # 各フィールドを比較
        for key in original_doc:
            if key in imported_doc:
                original_value = original_doc[key]
                imported_value = imported_doc[key]
                original_type = type(original_value).__name__
                imported_type = type(imported_value).__name__

                # 値と型が一致するか確認
                values_match = original_value == imported_value
                types_match = original_type == imported_type

                status = "一致" if values_match and types_match else "不一致"
                print(f"  {key}: {status}")

                if not values_match or not types_match:
                    print(f"    元の値: {original_value} (型: {original_type})")
                    print(f"    インポート後の値: {imported_value} (型: {imported_type})")
        print()
    else:
        print(f"ドキュメントID: {doc_id} - インポート後に見つかりません")
        print()

for doc_id in imported_docs_dict:
    if doc_id not in original_docs:
        print(f"ドキュメントID: {doc_id} - 元のデータには存在しません")
        print()
