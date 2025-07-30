import os
import datetime
from storekiss.crud import LiteStore
from storekiss.litestore import CollectionReference

# tests/temp_test_data ディレクトリにテスト用のデータベースファイルを生成
os.makedirs("tests/temp_test_data", exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
db_path = os.path.join("tests/temp_test_data", f"test_collection_{timestamp}.sqlite")

# 既存のファイルがあれば削除
if os.path.exists(db_path):
    os.remove(db_path)

# LiteStoreインスタンスを作成
db = LiteStore(db_path=db_path)

# コレクションを取得（CollectionReferenceを使用）
coll_ref = db.collection("test_collection")
print(f"コレクションリファレンスの型: {type(coll_ref)}")

# ドキュメントを作成
doc = coll_ref.document("doc1")
doc.set({"name": "テスト1", "value": 123})
print(f"ドキュメント1の内容: {doc.get()}")

# もう1つドキュメントを追加
doc2 = coll_ref.document("doc2")
doc2.set({"name": "テスト2", "value": 456})
print(f"ドキュメント2の内容: {doc2.get()}")

# コレクション内のすべてのドキュメントを取得
docs = coll_ref.get()
print(f"コレクション内のドキュメント数: {len(docs)}")
print(f"すべてのドキュメント: {docs}")

# 内部のコレクションオブジェクトを直接使用
internal_coll = coll_ref._collection
print(f"内部コレクションの型: {type(internal_coll)}")
internal_docs = internal_coll.get()
print(f"内部コレクションのドキュメント数: {len(internal_docs)}")
print(f"内部コレクションのドキュメント: {internal_docs}")
