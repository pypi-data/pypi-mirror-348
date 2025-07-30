"""
storekissライブラリでcollection.stream()とdoc.reference.update()を使用するテスト

このスクリプトは、storekissライブラリを使用して、Firestoreと同様の
collection.stream()でドキュメントを取得し、doc.reference.update()で更新する方法をテストします。
"""

import os
import uuid
import time
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
                raise ValueError(f"ドキュメントIDが設定されていません")
            
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
    
    def new_stream(self):
        # 元のstreamメソッドを呼び出す
        docs = list(original_stream(self))
        
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

def test_stream_update():
    """
    collection.stream()とdoc.reference.update()を使用したテスト
    """
    # パッチを適用
    apply_firestore_compatible_patch()
    
    # データベースファイルのパス
    db_path = "stream_update_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = Client(db_path)
    
    # コレクション名
    collection_name = 'test_items'
    collection = db.collection(collection_name)
    
    # テストデータを作成
    logger.info("テストデータを作成します")
    doc_ids = []
    for i in range(10):
        doc_id = str(uuid.uuid4())
        doc_ids.append(doc_id)
        collection.document(doc_id).set({
            'name': f'Item {i}',
            'value': i * 10,
            'active': True,
            'somfield': True  # 初期値はTrue
        })
        logger.info("ドキュメント %s を作成しました", doc_id)
    
    # stream()メソッドを使用してドキュメントをストリーミング処理
    logger.info("\nstream()メソッドを使用してドキュメントを取得し、doc.reference.update()で更新")
    count = 0
    start_time = time.time()
    
    # ドキュメントを取得
    docs = list(collection.stream())
    logger.info(f"{len(docs)}件のドキュメントを取得しました")
    
    # ユーザーが要求した形式のコード
    for doc in docs:
        # doc.reference.update()を使用してドキュメントを更新
        # フォールバック処理は行わず、必ずdoc.reference.update()を使用
        doc.reference.update({"somfield": False})
        count += 1
        logger.info("ドキュメント %s を更新しました (somfield=False)", doc.id)
    
    end_time = time.time()
    logger.info("更新完了: %d件 (所要時間: %.3f秒)", count, end_time - start_time)
    
    # 更新後のドキュメントを確認
    logger.info("\n更新後のドキュメントを確認")
    updated_docs = collection.get()
    success_count = 0
    for doc in updated_docs:
        doc_data = doc.to_dict()
        logger.info("ドキュメントID: %s, データ: %s", doc.id, doc_data)
        
        # somfieldフィールドが正しく更新されているか確認
        if doc_data.get('somfield') is False:
            logger.info("✓ somfieldフィールドが正しく更新されています")
            success_count += 1
        else:
            logger.error("✗ somfieldフィールドが更新されていません")
    
    # 結果を表示
    if success_count == len(doc_ids):
        logger.info("\n✅ すべてのドキュメントが正しく更新されました (%d/%d)", success_count, len(doc_ids))
    else:
        logger.error("\n❌ 一部のドキュメントが更新されていません (%d/%d)", success_count, len(doc_ids))

if __name__ == "__main__":
    test_stream_update()
