"""
storekissライブラリで並列処理を使用して大量のドキュメントを効率的に更新するテスト

このスクリプトは、storekissライブラリを使用して、並列処理により大量のドキュメントを
効率的に更新する方法を示します。
"""

import os
import uuid
import time
import concurrent.futures
from storekiss.litestore import Client
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Firestoreと互換性のあるパッチを適用
def apply_firestore_compatible_patch():
    """
    storekissライブラリにFirestoreと互換性のあるパッチを適用します。
    
    このパッチにより、DocumentSnapshotクラスにreferenceプロパティが追加され、
    Firestoreと同様にdoc.reference.update()の構文が使えるようになります。
    """
    # DocumentSnapshotクラスを取得
    from storekiss.crud import DocumentSnapshot
    from storekiss.litestore import DocumentReference, CollectionReference
    from storekiss.crud import Document
    
    # 元のDocumentSnapshotクラスを保存
    original_init = DocumentSnapshot.__init__
    
    # 新しい__init__メソッドを定義
    def new_init(self, data, id=None, collection=None, store=None):
        # 元の__init__メソッドを呼び出す
        if hasattr(original_init, '__code__') and original_init.__code__.co_argcount > 3:
            # 既に拡張されたinitメソッドの場合
            original_init(self, data, id, collection, store)
        else:
            # オリジナルのinitメソッドの場合
            original_init(self, data, id)
            # 追加の属性を設定
            self._collection = collection
            self._store = store
        self._reference = None
    
    # referenceプロパティを定義
    def reference_property(self):
        """
        ドキュメント参照を返します。
        
        Returns:
            DocumentReference: ドキュメント参照
            
        Raises:
            ValueError: ドキュメント参照の作成に必要な情報が不足している場合
        """
        if not hasattr(self, '_reference') or self._reference is None:
            # 必要な情報があるか確認
            if not hasattr(self, '_id') or self._id is None:
                raise ValueError("ドキュメントIDが設定されていません")
            
            if not hasattr(self, '_collection') or self._collection is None:
                raise ValueError(f"ドキュメントのコレクション名が設定されていません: id={self._id}")
            
            if not hasattr(self, '_store') or self._store is None:
                raise ValueError(f"ドキュメントのストアオブジェクトが設定されていません: id={self._id}, collection={self._collection}")
            
            # Documentオブジェクトを作成
            doc = Document(self._store, self._collection, self._id)
            # DocumentReferenceオブジェクトを作成
            self._reference = DocumentReference(doc)
            logger.debug(f"ドキュメント参照を作成しました: id={self._id}, collection={self._collection}")
        
        return self._reference
    
    # DocumentSnapshotクラスに新しいメソッドとプロパティを追加
    DocumentSnapshot.__init__ = new_init
    if not hasattr(DocumentSnapshot, 'reference') or not isinstance(DocumentSnapshot.reference, property):
        DocumentSnapshot.reference = property(reference_property)
    
    # CollectionReference.stream メソッドを拡張して、ドキュメントスナップショットに正しい情報を設定
    original_stream = CollectionReference.stream
    
    def new_stream(self, batch_size=20):
        # 元のstreamメソッドを呼び出す
        docs = list(original_stream(self, batch_size=batch_size))
        
        # コレクション名とストアオブジェクトを取得
        collection_name = self._collection.name
        store = self._collection.store
        
        if collection_name is None:
            raise ValueError("CollectionReferenceのコレクション名が取得できません")
        
        if store is None:
            raise ValueError("CollectionReferenceのストアオブジェクトが取得できません")
        
        logger.debug(f"コレクション名: {collection_name}, ストア: {store is not None}")
        
        # 各ドキュメントに必要な情報を設定
        result_docs = []
        for doc in docs:
            # 必要な情報を必ず設定
            doc._collection = collection_name
            doc._store = store
            result_docs.append(doc)
            logger.debug(f"ドキュメント情報を設定しました: id={doc.id}, collection={doc._collection}, store={doc._store is not None}")
        
        return result_docs
    
    # CollectionReference.streamメソッドを置き換える
    CollectionReference.stream = new_stream
    
    # Document.getメソッドを修正して、collection名とstoreオブジェクトを渡すようにする
    original_document_get = Document.get
    
    def new_document_get(self):
        """Get the document data as a DocumentSnapshot (Firestore互換)."""
        original_collection = self.store.default_collection
        self.store.default_collection = self.collection
        try:
            data = self.store.read(self.id)
            # DocumentSnapshotオブジェクトを作成するときに、collection名とstoreオブジェクトも渡す
            return DocumentSnapshot(data, id=self.id, collection=self.collection, store=self.store)
        except Exception as e:
            logger.error(f"Document.getメソッドで例外が発生: {str(e)}")
            raise
        finally:
            self.store.default_collection = original_collection
    
    # Document.getメソッドを置き換える
    Document.get = new_document_get
    
    logger.info("Firestoreと互換性のあるパッチを適用しました")
    return True

def update_document(doc):
    """
    ドキュメントを更新する関数（並列処理で使用）
    
    Args:
        doc: 更新するドキュメント
        
    Returns:
        tuple: (ドキュメントID, 成功したかどうか)
    """
    try:
        doc.reference.update({"updated": True, "timestamp": time.time()})
        return (doc.id, True)
    except Exception as e:
        logger.error(f"ドキュメント {doc.id} の更新中にエラーが発生しました: {str(e)}")
        return (doc.id, False)

def test_parallel_stream_update():
    """
    並列処理を使用した大量ドキュメントの更新テスト
    """
    # パッチを適用
    apply_firestore_compatible_patch()
    
    # データベースファイルのパス
    db_path = "parallel_stream_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = Client(db_path)
    
    # コレクション名
    collection_name = 'large_collection'
    collection = db.collection(collection_name)
    
    # テストデータ数
    doc_count = 500
    
    # テストデータを作成
    logger.info(f"{doc_count}件のテストデータを作成します")
    doc_ids = []
    start_time = time.time()
    
    for i in range(doc_count):
        doc_id = str(uuid.uuid4())
        doc_ids.append(doc_id)
        collection.document(doc_id).set({
            'name': f'Item {i}',
            'value': i,
            'active': True,
            'updated': False
        })
        
        # 進捗を表示
        if (i + 1) % 100 == 0 or i == doc_count - 1:
            logger.info(f"{i + 1}件のドキュメントを作成しました")
    
    end_time = time.time()
    logger.info(f"データ作成完了: {doc_count}件 (所要時間: {end_time - start_time:.3f}秒)")
    
    # 並列処理のワーカー数
    max_workers = 8
    
    # バッチサイズ
    batch_size = 100
    
    # stream()メソッドを使用してドキュメントをストリーミング処理
    logger.info(f"\n並列処理でドキュメントを更新 (ワーカー数: {max_workers}, バッチサイズ: {batch_size})")
    start_time = time.time()
    
    # 全ドキュメントを取得
    all_docs = list(collection.stream(batch_size=batch_size))
    logger.info(f"{len(all_docs)}件のドキュメントを取得しました")
    
    # 並列処理で更新
    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 各ドキュメントの更新タスクを作成
        future_to_doc = {executor.submit(update_document, doc): doc for doc in all_docs}
        
        # 結果を処理
        for i, future in enumerate(concurrent.futures.as_completed(future_to_doc)):
            doc = future_to_doc[future]
            try:
                doc_id, success = future.result()
                if success:
                    success_count += 1
                
                # 進捗を表示
                if (i + 1) % 100 == 0 or i == len(all_docs) - 1:
                    logger.info(f"{i + 1}/{len(all_docs)}件処理しました (成功: {success_count}件)")
            except Exception as e:
                logger.error(f"ドキュメント {doc.id} の処理中に例外が発生しました: {str(e)}")
    
    end_time = time.time()
    logger.info(f"更新完了: {success_count}/{len(all_docs)}件 (所要時間: {end_time - start_time:.3f}秒)")
    
    # 更新後のドキュメントを確認
    logger.info("\n更新後のドキュメントを確認")
    updated_count = 0
    check_start_time = time.time()
    
    # バッチで確認
    offset = 0
    while True:
        # バッチを取得
        batch = list(collection.limit(batch_size).offset(offset).get())
        if not batch:
            break
            
        # バッチ内のドキュメントを確認
        for doc in batch:
            doc_data = doc.to_dict()
            if doc_data.get('updated') is True:
                updated_count += 1
        
        # 進捗を表示
        offset += len(batch)
        logger.info(f"{offset}件確認しました (更新済み: {updated_count}件)")
        
        # 取得したドキュメント数がバッチサイズより少ない場合は終了
        if len(batch) < batch_size:
            break
    
    check_end_time = time.time()
    
    # 結果を表示
    if updated_count == doc_count:
        logger.info(f"\n✅ すべてのドキュメントが正しく更新されました ({updated_count}/{doc_count})")
    else:
        logger.error(f"\n❌ 一部のドキュメントが更新されていません ({updated_count}/{doc_count})")
    
    logger.info(f"確認完了: 所要時間: {check_end_time - check_start_time:.3f}秒")
    logger.info(f"合計処理時間: {(end_time - start_time) + (check_end_time - check_start_time):.3f}秒")

if __name__ == "__main__":
    test_parallel_stream_update()
