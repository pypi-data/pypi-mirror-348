"""
storekissライブラリにより本格的なstream()メソッドを実装する例

このスクリプトでは、storekissライブラリのCollectionReferenceクラスに
Firestoreのような遅延読み込みを行うstream()メソッドを実装する方法を示します。
"""

import os
import uuid
from typing import Iterator, Optional, Any, Dict, List
from storekiss import litestore
from storekiss.litestore import CollectionReference, DocumentSnapshot
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 元のCollectionReferenceクラスのget()メソッドを保存
original_get = CollectionReference.get

# 改良版stream()メソッドの実装
def improved_stream(self, batch_size: int = 10) -> Iterator[DocumentSnapshot]:
    """
    コレクション内のすべてのドキュメントをストリームとして取得します。
    
    このメソッドは、大量のドキュメントを効率的に処理するために、
    バッチ単位で遅延読み込みを行います。一度にすべてのドキュメントを
    メモリに読み込むのではなく、必要に応じて少しずつ取得します。
    
    Args:
        batch_size: 一度に取得するドキュメントの数
        
    Returns:
        Iterator[DocumentSnapshot]: ドキュメントのイテレータ
    """
    # 現在処理中のオフセット
    offset = 0
    
    while True:
        # バッチサイズ分のドキュメントを取得するクエリを作成
        query = self.limit(batch_size)
        
        # オフセットが必要な場合は、スキップするロジックを追加
        # 注: 実際のFirestoreではカーソルベースのページネーションを使用
        # storekissでは簡易的な実装としてオフセットを使用
        if offset > 0:
            # 注: ここでは簡易的な実装のため、実際にはoffsetをサポートするメソッドが
            # storekissに必要になります。この例では概念実装として示しています。
            # query = query.offset(offset)  # 実際にはこのようなメソッドが必要
            pass
        
        # クエリを実行してバッチを取得
        batch = query.get()
        
        # 結果が空の場合は終了
        if not batch:
            break
            
        # 各ドキュメントを順番に返す
        for doc in batch:
            yield doc
            
        # 次のバッチのためにオフセットを更新
        offset += len(batch)
        
        # 取得したドキュメント数がバッチサイズより少ない場合は、
        # これ以上のドキュメントがないと判断して終了
        if len(batch) < batch_size:
            break

# 実際のstorekissライブラリに実装する場合のコード例
def implement_improved_stream():
    """
    storekissライブラリに改良版stream()メソッドを実装する例
    """
    # CollectionReferenceクラスにstream()メソッドを追加
    CollectionReference.stream = improved_stream
    
    # Queryクラスにもstream()メソッドを追加する必要があります
    # (実際の実装では必要になりますが、この例では省略)

def test_improved_stream():
    """改良版stream()メソッドのテスト"""
    # データベースファイルのパス
    db_path = "improved_stream_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_improved_stream'
    collection_ref = db.collection(collection_name)
    
    # テストデータを作成
    logger.info("テストデータを作成します")
    for i in range(25):  # より多くのテストデータを作成
        doc_id = str(uuid.uuid4())
        collection_ref.document(doc_id).set({
            'name': f'Document {i}',
            'value': i * 10
        })
        logger.info("ドキュメント %s を作成しました", doc_id)
    
    # 改良版stream()メソッドを実装
    implement_improved_stream()
    
    # バッチサイズを指定してstream()メソッドを使用
    logger.info("\n改良版stream()メソッドを使用してドキュメントを取得 (バッチサイズ: 5)")
    batch_size = 5
    docs = collection_ref.stream(batch_size)
    
    # 各ドキュメントに check=True を設定
    count = 0
    for doc in docs:
        doc_id = doc.id
        doc_ref = collection_ref.document(doc_id)
        doc_ref.update({'check': True})
        logger.info("ドキュメント %s を更新しました (check=True) - バッチ %d", 
                   doc_id, count // batch_size + 1)
        count += 1
    
    logger.info("合計 %d 件のドキュメントを処理しました", count)
    
    # 更新後のドキュメントを確認
    logger.info("\n更新後のドキュメントを確認")
    updated_count = 0
    for doc in collection_ref.stream(batch_size):
        doc_data = doc.to_dict()
        if doc_data.get('check') is True:
            updated_count += 1
    
    logger.info("check=True が設定されたドキュメント: %d/%d", updated_count, count)
    if updated_count == count:
        logger.info("✓ すべてのドキュメントが正しく更新されました")
    else:
        logger.error("✗ 一部のドキュメントが更新されていません")

# 注: この実装はstorekissの現在の機能に基づいた概念実装です。
# 実際に動作させるには、storekissライブラリにoffsetのサポートなど
# 追加の機能実装が必要になります。

if __name__ == "__main__":
    # 実際のテスト実行は、storekissライブラリの拡張後に行ってください
    print("このスクリプトは概念実装です。実際に動作させるには、storekissライブラリの拡張が必要です。")
    print("実装の参考としてご利用ください。")
