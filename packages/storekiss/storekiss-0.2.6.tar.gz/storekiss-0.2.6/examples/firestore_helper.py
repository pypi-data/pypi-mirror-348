"""
storekissライブラリでFirestoreと同様の使い方をサポートするヘルパー関数

このモジュールは、storekissライブラリを使用して、Firestoreと同様の
doc.reference.update()のような構文をサポートするためのヘルパー関数を提供します。
"""

import os
import uuid
import time
from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class FirestoreHelper:
    """
    storekissライブラリでFirestoreと同様の使い方をサポートするヘルパークラス
    """
    
    @staticmethod
    def update_documents(docs, update_data):
        """
        ドキュメントのコレクションを更新します。
        
        Firestoreと同様に、doc.reference.update()の代わりに使用できます。
        
        Args:
            docs: ドキュメントのコレクション（stream()またはget()の結果）
            update_data: 更新するデータ（辞書形式）
            
        Returns:
            更新されたドキュメント数
        """
        count = 0
        for doc in docs:
            # ドキュメントIDとコレクション情報を取得
            doc_id = doc.id
            # コレクション名を取得（ドキュメントから直接取得できないため、推測する）
            collection_name = None
            
            # ドキュメントからコレクション名を取得する方法を探す
            if hasattr(doc, '_collection'):
                collection_name = doc._collection
            elif hasattr(doc, 'collection'):
                collection_name = doc.collection
                
            # コレクション名が取得できない場合は、エラーログを出力してスキップ
            if collection_name is None:
                logger.error("ドキュメント %s のコレクション名を取得できませんでした", doc_id)
                continue
                
            # ドキュメントを更新
            try:
                # ドキュメントを取得したクライアントを特定
                if hasattr(doc, '_store'):
                    store = doc._store
                    # コレクションを取得
                    collection_ref = store.collection(collection_name)
                    # ドキュメントを更新
                    collection_ref.document(doc_id).update(update_data)
                    count += 1
                else:
                    # クライアントが取得できない場合は、デフォルトのクライアントを使用
                    client = litestore.Client()
                    collection_ref = client.collection(collection_name)
                    collection_ref.document(doc_id).update(update_data)
                    count += 1
            except Exception as e:
                logger.error("ドキュメント %s の更新中にエラーが発生しました: %s", doc_id, str(e))
                
        return count

def test_firestore_helper():
    """
    FirestoreHelperクラスをテストします。
    """
    # データベースファイルのパス
    db_path = "firestore_helper_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_firestore_helper'
    collection_ref = db.collection(collection_name)
    
    # テストデータを作成
    logger.info("テストデータを作成します")
    doc_ids = []
    for i in range(5):
        doc_id = str(uuid.uuid4())
        doc_ids.append(doc_id)
        collection_ref.document(doc_id).set({
            'name': f'Document {i}',
            'value': i * 10
        })
        logger.info("ドキュメント %s を作成しました", doc_id)
    
    # stream()メソッドを使用してすべてのドキュメントを取得
    logger.info("\nstream()メソッドを使用してドキュメントを取得")
    docs = collection_ref.stream()
    
    # FirestoreHelperを使用して更新
    logger.info("\nFirestoreHelperを使用して更新: FirestoreHelper.update_documents()")
    start_time = time.time()
    count = FirestoreHelper.update_documents(docs, {'check': True})
    end_time = time.time()
    logger.info("更新完了: %d件 (所要時間: %.3f秒)", count, end_time - start_time)
    
    # 更新後のドキュメントを確認
    logger.info("\n更新後のドキュメントを確認")
    updated_docs = collection_ref.get()
    success_count = 0
    for doc in updated_docs:
        doc_data = doc.to_dict()
        logger.info("ドキュメントID: %s, データ: %s", doc.id, doc_data)
        
        # checkフィールドが正しく設定されているか確認
        if doc_data.get('check') is True:
            logger.info("✓ checkフィールドが正しく設定されています")
            success_count += 1
        else:
            logger.error("✗ checkフィールドが設定されていません")
    
    # 結果を表示
    if success_count == len(doc_ids):
        logger.info("\n✅ すべてのドキュメントが正しく更新されました (%d/%d)", success_count, len(doc_ids))
    else:
        logger.error("\n❌ 一部のドキュメントが更新されていません (%d/%d)", success_count, len(doc_ids))

if __name__ == "__main__":
    test_firestore_helper()
