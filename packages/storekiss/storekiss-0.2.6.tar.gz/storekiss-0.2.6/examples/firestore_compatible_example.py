"""
storekissライブラリでFirestoreと同様の使い方をする例

このスクリプトは、storekissライブラリを使用して、Firestoreと同様の
doc.reference.update()のような構文を実現する方法を示します。
"""

import os
import uuid
import time
from storekiss.litestore import Client
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def test_firestore_compatible_usage():
    """
    storekissライブラリでFirestoreと同様の使い方をテストします。
    """
    # データベースファイルのパス
    db_path = "firestore_compatible_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = Client(db_path)
    
    # コレクション名
    collection_name = 'eqevent'
    collection = db.collection(collection_name)
    
    # テストデータを作成
    logger.info("テストデータを作成します")
    doc_ids = []
    for i in range(5):
        doc_id = str(uuid.uuid4())
        doc_ids.append(doc_id)
        collection.document(doc_id).set({
            'name': f'Earthquake {i}',
            'magnitude': 5.0 + i * 0.5,
            'is_mainshock': True
        })
        logger.info("ドキュメント %s を作成しました", doc_id)
    
    # stream()メソッドを使用してドキュメントをストリーミング処理
    logger.info("\nstream()メソッドを使用してドキュメントを取得")
    count = 0
    start_time = time.time()
    
    # Firestoreと同様の使い方
    for doc in collection.stream():
        # ドキュメントIDを取得
        doc_id = doc.id
        # ドキュメント参照を取得（Firestoreと異なり、doc.referenceは使用できないため）
        doc_ref = collection.document(doc_id)
        # updateメソッドを使用して特定のフィールドのみを更新
        doc_ref.update({"is_mainshock": False})
        count += 1
        logger.info("ドキュメント %s を更新しました (is_mainshock=False)", doc_id)
    
    end_time = time.time()
    logger.info("更新完了: %d件 (所要時間: %.3f秒)", count, end_time - start_time)
    
    # 更新後のドキュメントを確認
    logger.info("\n更新後のドキュメントを確認")
    updated_docs = collection.get()
    success_count = 0
    for doc in updated_docs:
        doc_data = doc.to_dict()
        logger.info("ドキュメントID: %s, データ: %s", doc.id, doc_data)
        
        # is_mainshockフィールドが正しく設定されているか確認
        if doc_data.get('is_mainshock') is False:
            logger.info("✓ is_mainshockフィールドが正しく設定されています")
            success_count += 1
        else:
            logger.error("✗ is_mainshockフィールドが設定されていません")
    
    # 結果を表示
    if success_count == len(doc_ids):
        logger.info("\n✅ すべてのドキュメントが正しく更新されました (%d/%d)", success_count, len(doc_ids))
    else:
        logger.error("\n❌ 一部のドキュメントが更新されていません (%d/%d)", success_count, len(doc_ids))

if __name__ == "__main__":
    test_firestore_compatible_usage()
