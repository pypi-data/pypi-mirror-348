"""
バッチ処理を使用してドキュメントを一括更新するサンプル

このスクリプトは、storekissライブラリのバッチ処理機能を使用して、
コレクション内の多数のドキュメントを効率的に更新する方法を示します。
"""

import os
import uuid
import time
from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_test_data(db, collection_name, document_count=100):
    """テスト用のデータを作成する"""
    collection_ref = db.collection(collection_name)
    
    logger.info("%d件のテストデータを作成します", document_count)
    
    for i in range(document_count):
        doc_id = str(uuid.uuid4())
        collection_ref.document(doc_id).set({
            'name': f'Document {i}',
            'value': i * 10,
            'created_at': time.time()
        })
        
    logger.info("テストデータの作成が完了しました")
    return collection_ref


def update_all_documents_in_batches(collection_ref, batch_size=20):
    """
    コレクション内のすべてのドキュメントをバッチ処理で更新する
    
    Args:
        collection_ref: 更新するコレクションの参照
        batch_size: バッチサイズ（デフォルト: 20）
    """
    # ドキュメントをストリームで取得
    docs = list(collection_ref.stream())
    
    # クライアントを取得
    db = litestore.Client()
    
    total_docs = len(docs)
    logger.info("%d件のドキュメントが見つかりました。バッチサイズ %d で更新します...", 
                total_docs, batch_size)
    
    # バッチサイズごとに処理
    for i in range(0, total_docs, batch_size):
        batch = db.batch()
        batch_docs = docs[i:i + batch_size]
        
        for doc in batch_docs:
            doc_ref = collection_ref.document(doc.id)
            batch.update(doc_ref, {"updated": True, "batch_number": i // batch_size + 1})
        
        # バッチをコミット
        batch.commit()
        logger.info("バッチ %d をコミットしました（%d件のドキュメント）", 
                    i // batch_size + 1, len(batch_docs))
    
    logger.info("すべてのドキュメントが更新されました")


def verify_updates(collection_ref):
    """更新が正しく行われたことを確認する"""
    updated_count = 0
    batch_counts = {}
    
    for doc in collection_ref.stream():
        doc_data = doc.to_dict()
        if doc_data.get("updated") is True:
            updated_count += 1
            
            batch_number = doc_data.get("batch_number", 0)
            if batch_number in batch_counts:
                batch_counts[batch_number] += 1
            else:
                batch_counts[batch_number] = 1
    
    total_docs = len(list(collection_ref.stream()))
    
    logger.info("更新の確認:")
    logger.info("  - 合計ドキュメント数: %d", total_docs)
    logger.info("  - 更新されたドキュメント数: %d", updated_count)
    logger.info("  - バッチごとのドキュメント数:")
    
    for batch_number, count in sorted(batch_counts.items()):
        logger.info("    - バッチ %d: %d件", batch_number, count)
    
    if updated_count == total_docs:
        logger.info("✅ すべてのドキュメントが正しく更新されました")
    else:
        logger.error("❌ 一部のドキュメントが更新されていません: %d/%d", 
                     updated_count, total_docs)


def main():
    """メイン関数"""
    # データベースファイルのパス
    db_path = "batch_update_example.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_batch_update'
    
    # テストデータを作成
    collection_ref = create_test_data(db, collection_name, document_count=100)
    
    # バッチ処理でドキュメントを更新
    update_all_documents_in_batches(collection_ref, batch_size=25)
    
    # 更新を確認
    verify_updates(collection_ref)


if __name__ == "__main__":
    main()
