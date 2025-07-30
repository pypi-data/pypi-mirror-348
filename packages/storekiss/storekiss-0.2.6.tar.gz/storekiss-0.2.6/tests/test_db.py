import os
import datetime
from storekiss.crud import LiteStore

# tests/temp_test_data ディレクトリにテスト用のデータベースファイルを生成
os.makedirs("tests/temp_test_data", exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
db_path = os.path.join("tests/temp_test_data", f"test_db_{timestamp}.sqlite")

# 既存のファイルがあれば削除
if os.path.exists(db_path):
    os.remove(db_path)

# LiteStoreインスタンスを作成
db = LiteStore(db_path=db_path)

# コレクションを取得
coll = db.get_collection("test")
print(f"コレクション名: {coll.name}")

# ドキュメントを作成
doc = coll.doc("doc1")
doc.set({"name": "テスト", "value": 123})
print(f"ドキュメントの内容: {doc.get()}")

# コレクション内のすべてのドキュメントを取得
docs = coll.get()
print(f"コレクション内のドキュメント数: {len(docs)}")
print(f"すべてのドキュメント: {docs}")
