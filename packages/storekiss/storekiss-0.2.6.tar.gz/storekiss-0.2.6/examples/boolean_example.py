#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ブール値の処理に関するサンプルコード
"""

import os
import json
import datetime
from pprint import pprint

from storekiss import litestore


# tests/temp_test_data ディレクトリに一時ファイルを作成
os.makedirs("tests/temp_test_data", exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
db_path = os.path.join("tests/temp_test_data", f"boolean_example_{timestamp}.db")

# Firestoreクライアントを作成
db = litestore.client(db_path=db_path, default_collection="users")

# ブール値を含むデータを追加
print("=== ブール値を含むデータを追加 ===")
user1 = db.collection("users").add(
    {"name": "ユーザー1", "is_active": True, "is_admin": False}
)
print(f"ユーザー1を追加しました: {user1}")

user2 = db.collection("users").add({"name": "ユーザー2", "is_active": False, "is_admin": False})
print(f"ユーザー2を追加しました: {user2}")

# データを取得して確認
print("\n=== データを取得して確認 ===")
users = db.collection("users").get()
for user in users:
    print(f"ID: {user['id']}, データ: {user}")

# ブール値でフィルタリング
print("\n=== ブール値でフィルタリング ===")
active_users = db.collection("users").where("is_active", "==", True).get()
print(f"アクティブなユーザー: {len(active_users)}件")
for user in active_users:
    print(f"ID: {user['id']}, データ: {user}")

# エクスポート/インポートでブール値の処理を確認
print("\n=== エクスポート/インポートでブール値の処理を確認 ===")
timestamp_export = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
export_dir = os.path.join("tests/temp_test_data", f"boolean_export_{timestamp_export}")
os.makedirs(export_dir, exist_ok=True)

# コレクションをエクスポート
metadata_file = db.export_collection("users", export_dir)
print(f"メタデータファイル: {metadata_file}")

# エクスポートされたJSONLファイルの内容を確認
jsonl_file = os.path.join(export_dir, "users", "users.jsonl")
print(f"JSONLファイル: {jsonl_file}")

with open(jsonl_file, "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)
        print("\nエクスポートされたドキュメント:")
        pprint(doc)

        # ブール値フィールドの型を確認
        if "is_active" in doc["fields"]:
            print(f"is_active フィールドの型: {list(doc['fields']['is_active'].keys())[0]}")
        if "is_admin" in doc["fields"]:
            print(f"is_admin フィールドの型: {list(doc['fields']['is_admin'].keys())[0]}")

# 新しいデータベースにインポート
timestamp_new = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
new_db_path = os.path.join(
    "tests/temp_test_data", f"boolean_example_new_{timestamp_new}.db"
)
new_db = litestore.client(
    db_path=new_db_path, default_collection="users"
)

# エクスポートしたデータをインポート
imported_count = new_db.import_collection("users", export_dir)
print(f"\nインポートされたドキュメント数: {imported_count}")

# インポートされたデータを確認
imported_users = new_db.collection("users").get()
print("\nインポートされたユーザー:")
for user in imported_users:
    print(f"ID: {user['id']}, データ: {user}")

# ブール値でフィルタリング（インポート後）
active_imported_users = new_db.collection("users").where("is_active", "==", True).get()
print(f"\nインポート後のアクティブなユーザー: {len(active_imported_users)}件")
for user in active_imported_users:
    print(f"ID: {user['id']}, データ: {user}")

# 一時ファイルを削除
os.unlink(db_path)
if os.path.exists(new_db_path):
    os.unlink(new_db_path)
