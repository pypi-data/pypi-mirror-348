"""
バッチ処理を行うstream()メソッドのテスト

このスクリプトは、storekissライブラリに実装したバッチ処理を行うstream()メソッドをテストします。
"""

import os
import uuid
import time
from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def test_batch_stream():
    """バッチ処理を行うstream()メソッドのテスト"""
    # データベースファイルのパス
    db_path = "batch_stream_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_batch_stream'
    collection_ref = db.collection(collection_name)
    
    # テストデータを作成（多めに作成）
    document_count = 50
    logger.info("%d件のテストデータを作成します", document_count)
    
    for i in range(document_count):
        doc_id = str(uuid.uuid4())
        collection_ref.document(doc_id).set({
            'name': f'Document {i}',
            'value': i * 10,
            'created_at': time.time()
        })
        logger.info("ドキュメント %s を作成しました (index: %d)", doc_id, i)
    
    # 通常のget()メソッドでドキュメントを取得
    start_time = time.time()
    all_docs = collection_ref.get()
    end_time = time.time()
    logger.info("\nget()メソッドで全件取得: %d件 (所要時間: %.3f秒)", 
               len(all_docs), end_time - start_time)
    
    # stream()メソッドを使用してドキュメントを取得（デフォルトバッチサイズ）
    logger.info("\nstream()メソッドでドキュメントを取得（デフォルトバッチサイズ）")
    start_time = time.time()
    count = 0
    for doc in collection_ref.stream():
        count += 1
        if count % 20 == 0:  # 20件ごとにログ出力
            logger.info("%d件のドキュメントを処理しました", count)
    end_time = time.time()
    logger.info("stream()メソッドで全件取得: %d件 (所要時間: %.3f秒)", 
               count, end_time - start_time)
    
    # 小さいバッチサイズでstream()メソッドを使用
    batch_size = 5
    logger.info("\nstream()メソッドでドキュメントを取得（バッチサイズ: %d）", batch_size)
    start_time = time.time()
    count = 0
    for doc in collection_ref.stream(batch_size=batch_size):
        count += 1
        if count % batch_size == 0:  # バッチサイズごとにログ出力
            logger.info("%d件のドキュメントを処理しました（バッチ: %d）", 
                       count, count // batch_size)
    end_time = time.time()
    logger.info("stream()メソッドで全件取得: %d件 (所要時間: %.3f秒)", 
               count, end_time - start_time)
    
    # whereクエリとstream()メソッドの組み合わせ
    logger.info("\nwhereクエリとstream()メソッドの組み合わせ")
    start_time = time.time()
    count = 0
    query = collection_ref.where('value', '>=', 250)
    for doc in query.stream(batch_size=10):
        doc_data = doc.to_dict()
        count += 1
        logger.info("ドキュメント %s: value = %d", doc.id, doc_data.get('value', 0))
    end_time = time.time()
    logger.info("whereクエリとstream()の組み合わせ: %d件 (所要時間: %.3f秒)", 
               count, end_time - start_time)
    
    # order_byとstream()メソッドの組み合わせ
    logger.info("\norder_byとstream()メソッドの組み合わせ")
    start_time = time.time()
    count = 0
    query = collection_ref.order_by('value', direction='DESC').limit(5)
    logger.info("value降順で上位5件を取得:")
    for doc in query.stream():
        doc_data = doc.to_dict()
        count += 1
        logger.info("ドキュメント %s: value = %d", doc.id, doc_data.get('value', 0))
    end_time = time.time()
    logger.info("order_byとstream()の組み合わせ: %d件 (所要時間: %.3f秒)", 
               count, end_time - start_time)
    
    # 各ドキュメントにcheck=Trueを設定
    logger.info("\n各ドキュメントにcheck=Trueを設定")
    start_time = time.time()
    count = 0
    for doc in collection_ref.stream(batch_size=10):
        doc_id = doc.id
        doc_ref = collection_ref.document(doc_id)
        doc_ref.update({'check': True})
        count += 1
        if count % 10 == 0:  # 10件ごとにログ出力
            logger.info("%d件のドキュメントを更新しました", count)
    end_time = time.time()
    logger.info("全件更新完了: %d件 (所要時間: %.3f秒)", count, end_time - start_time)
    
    # 更新の確認
    logger.info("\n更新の確認")
    checked_count = 0
    for doc in collection_ref.stream():
        doc_data = doc.to_dict()
        if doc_data.get('check') is True:
            checked_count += 1
    
    if checked_count == document_count:
        logger.info("✅ すべてのドキュメントが正しく更新されました: %d/%d", 
                   checked_count, document_count)
    else:
        logger.error("❌ 一部のドキュメントが更新されていません: %d/%d", 
                    checked_count, document_count)


if __name__ == "__main__":
    test_batch_stream()
