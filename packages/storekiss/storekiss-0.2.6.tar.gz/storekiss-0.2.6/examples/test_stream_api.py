"""
storekissのAPIでドキュメントの取得と更新をテストするスクリプト
"""

import os
import uuid
from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    # データベースファイルのパス
    db_path = "test_stream_api.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_documents'
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
    
    # 方法1: get()メソッドを使用してすべてのドキュメントを取得
    logger.info("\n方法1: get()メソッドを使用")
    docs = collection_ref.get()
    logger.info("%d件のドキュメントを取得しました", len(docs))
    
    for doc in docs:
        # DocumentSnapshotオブジェクトの属性を調査
        logger.info("ドキュメントの型: %s", type(doc).__name__)
        logger.info("ドキュメントの属性: %s", dir(doc))
        
        try:
            # いくつかの方法を試す
            if hasattr(doc, 'id'):
                if callable(doc.id):
                    doc_id = doc.id()
                else:
                    doc_id = doc.id
            elif hasattr(doc, '__getitem__'):
                try:
                    doc_id = doc['id']
                except (TypeError, KeyError):
                    doc_id = None
            else:
                doc_id = str(doc)
                
            logger.info("取得したドキュメントID: %s", doc_id)
            
            # ドキュメントデータの取得を試みる
            if hasattr(doc, 'to_dict'):
                if callable(doc.to_dict):
                    doc_data = doc.to_dict()
                    logger.info("to_dict()の結果: %s", doc_data)
            
            # ドキュメントを更新
            if doc_id:
                doc_ref = collection_ref.document(doc_id)
                doc_ref.update({'check1': True})
                logger.info("ドキュメント %s を更新しました (check1=True)", doc_id)
        except Exception as e:
            logger.error("エラー: %s", str(e))
    
    # 方法2: streamメソッドがあるか試してみる
    logger.info("\n方法2: streamメソッドを試す")
    try:
        docs = collection_ref.stream()
        for doc in docs:
            doc_id = getattr(doc, 'id', None)
            logger.info("ドキュメントID: %s", doc_id)
            
            # referenceプロパティがあるか確認
            if hasattr(doc, 'reference'):
                doc.reference.update({'check2': True})
                logger.info("ドキュメント %s を更新しました (check2=True)", doc_id)
            else:
                logger.warning("doc.referenceプロパティがありません")
    except AttributeError:
        logger.error("streamメソッドはstorekissでは利用できません")
    except Exception as e:
        logger.error("エラーが発生しました: %s", str(e))
    
    # 方法3: ドキュメントを直接取得して更新
    logger.info("\n方法3: ドキュメントを直接取得して更新")
    docs = collection_ref.get()
    for doc in docs:
        # DocumentSnapshotからIDを取得
        doc_id = doc.id
        
        # ドキュメントリファレンスを取得
        doc_ref = collection_ref.document(doc_id)
        
        # ドキュメントの現在の状態を取得
        doc_snapshot = doc_ref.get()
        doc_data = doc_snapshot.to_dict()
        logger.info("ドキュメントID: %s, データ: %s", doc_id, doc_data)
        
        # ドキュメントを更新
        doc_ref.update({'check3': True})
        logger.info("ドキュメント %s を更新しました (check3=True)", doc_id)
    
    # 最終的な状態を確認
    logger.info("\n最終状態の確認")
    final_docs = collection_ref.get()
    for doc in final_docs:
        doc_id = doc.id
        doc_data = doc.to_dict()
        logger.info("ドキュメントID: %s, データ: %s", doc_id, doc_data)

if __name__ == "__main__":
    main()
