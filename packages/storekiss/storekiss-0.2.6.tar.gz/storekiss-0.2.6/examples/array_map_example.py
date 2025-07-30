"""
配列（リスト）とマップ（辞書）の拡張機能を示す例

このサンプルでは、以下の機能を示します：
1. 配列の型チェック
2. 配列の contains クエリ
3. 多次元配列のサポート
4. ネストされたフィールドへのアクセス（ドット表記）
5. マップの部分更新
"""

import sys
import datetime
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from storekiss.litestore import client
from storekiss.validation import ListField, MapField, StringField, NumberField, Schema

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def array_example():
    """配列（リスト）の拡張機能を示す例"""
    logging.info("=== 配列（リスト）の拡張機能の例 ===")
    
    schema = Schema({
        "tags": ListField(element_type=str),  # 文字列のみを含む配列
        "scores": ListField(element_type=int),  # 整数のみを含む配列
        "mixed": ListField(),  # 任意の型を含む配列
        "matrix": ListField(  # 2次元配列（数値のリストのリスト）
            item_validator=ListField(element_type=float)
        ),
    })
    
    db = client(db_path="array_example.db")
    collection = db.collection("arrays")
    
    valid_data = {
        "tags": ["python", "database", "sqlite"],
        "scores": [85, 92, 78, 95],
        "mixed": ["text", 123, True, None, {"key": "value"}],
        "matrix": [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0]
        ]
    }
    
    doc_ref = collection.add(valid_data)
    logging.info(f"有効なデータを追加しました: {doc_ref}")
    
    try:
        invalid_data = {
            "tags": ["python", 123, "sqlite"],  # 数値が含まれている（文字列のみ許可）
            "scores": [85, 92.5, 78],  # 浮動小数点数が含まれている（整数のみ許可）
        }
        collection.add(invalid_data)
    except Exception as e:
        logging.info(f"予想通りエラーが発生しました: {e}")
    
    python_docs = collection.where("tags", "contains", "python").get()
    logging.info(f"'python'タグを含むドキュメント数: {len(python_docs)}")
    
    high_score_docs = collection.where("scores", "contains", 95).get()
    logging.info(f"95点を含むドキュメント数: {len(high_score_docs)}")
    
    no_docs = collection.where("tags", "contains", "java").get()
    logging.info(f"'java'タグを含むドキュメント数: {len(no_docs)}")


def map_example():
    """マップ（辞書）の拡張機能を示す例"""
    logging.info("\n=== マップ（辞書）の拡張機能の例 ===")
    
    schema = Schema({
        "name": StringField(),
        "age": NumberField(integer_only=True),
        "address.street": StringField(),  # ドット表記でネストされたフィールドを指定
        "address.city": StringField(),
        "address.zip": StringField(required=False),
        "contact.email": StringField(),
        "contact.phone": StringField(required=False),
    })
    
    db = client(db_path="map_example.db")
    collection = db.collection("users")
    
    user_data = {
        "name": "山田太郎",
        "age": 35,
        "address": {
            "street": "桜木町1-2-3",
            "city": "東京都",
            "zip": "123-4567"
        },
        "contact": {
            "email": "yamada@example.com",
            "phone": "03-1234-5678"
        }
    }
    
    doc_ref = collection.add(user_data)
    doc_id = doc_ref.id
    logging.info(f"ユーザーデータを追加しました: {doc_id}")
    
    tokyo_users = collection.where("address.city", "==", "東京都").get()
    logging.info(f"東京都に住むユーザー数: {len(tokyo_users)}")
    
    user_doc = collection.document(doc_id)
    user_doc.update({
        "address.street": "新宿区1-2-3",  # 住所の一部だけを更新
        "contact.phone": "090-1234-5678"  # 電話番号だけを更新
    })
    
    updated_user = user_doc.get().to_dict()
    logging.info(f"更新後の住所: {updated_user['address']}")
    logging.info(f"更新後の連絡先: {updated_user['contact']}")


if __name__ == "__main__":
    array_example()
    map_example()
