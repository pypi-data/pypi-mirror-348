"""
stream()メソッドのテスト

このスクリプトは、storekissライブラリに実装したstream()メソッドをテストします。
"""

import os
import uuid
from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def test_stream_method():
    """stream()メソッドのテスト"""
    # データベースファイルのパス
    db_path = "stream_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_stream'
    collection_ref = db.collection(collection_name)
    
    # テストデータを作成
    logger.info("テストデータを作成します")
    for i in range(5):
        doc_id = str(uuid.uuid4())
        collection_ref.document(doc_id).set({
            'name': f'Document {i}',
            'value': i * 10
        })
        logger.info("ドキュメント %s を作成しました", doc_id)
    
    # stream()メソッドを使用してすべてのドキュメントを取得
    logger.info("\nstream()メソッドを使用してドキュメントを取得")
    docs = collection_ref.stream()
    
    # 各ドキュメントに check=True を設定
    for doc in docs:
        doc_id = doc.id
        doc_ref = collection_ref.document(doc_id)
        doc_ref.update({'check': True})
        logger.info("ドキュメント %s を更新しました (check=True)", doc_id)
    
    # 更新後のドキュメントを確認
    logger.info("\n更新後のドキュメントを確認")
    updated_docs = collection_ref.get()
    for doc in updated_docs:
        doc_data = doc.to_dict()
        logger.info("ドキュメントID: %s, データ: %s", doc.id, doc_data)
        
        # checkフィールドが正しく設定されているか確認
        if doc_data.get('check') is True:
            logger.info("✓ checkフィールドが正しく設定されています")
        else:
            logger.error("✗ checkフィールドが設定されていません")


if __name__ == "__main__":
    test_stream_method()
