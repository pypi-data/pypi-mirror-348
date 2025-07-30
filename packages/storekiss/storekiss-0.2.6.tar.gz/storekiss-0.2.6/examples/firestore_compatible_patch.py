"""
storekissライブラリにFirestoreと互換性のあるdoc.reference.update()をサポートするためのパッチ

このスクリプトは、storekissライブラリのDocumentSnapshotクラスにreferenceプロパティを追加し、
Firestoreと同様にdoc.reference.update()の構文をサポートするようにします。
"""

import os
import uuid
import time
from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def apply_firestore_compatible_patch():
    """
    storekissライブラリにFirestoreと互換性のあるパッチを適用します。
    
    このパッチにより、DocumentSnapshotクラスにreferenceプロパティが追加され、
    Firestoreと同様にdoc.reference.update()の構文が使えるようになります。
    """
    # DocumentSnapshotクラスを取得
    from storekiss.crud import DocumentSnapshot
    
    # 元のDocumentSnapshotクラスを保存
    original_init = DocumentSnapshot.__init__
    
    # 新しい__init__メソッドを定義
    def new_init(self, data, id=None, collection=None, store=None):
        # 元の__init__メソッドを呼び出す
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
        """
        if not hasattr(self, '_reference') or self._reference is None:
            if hasattr(self, '_id') and self._id is not None and hasattr(self, '_collection') and self._collection is not None and hasattr(self, '_store') and self._store is not None:
                # 遅延インポートを使用して循環インポートを回避
                from storekiss.litestore import DocumentReference
                from storekiss.crud import Document
                # Documentオブジェクトを作成
                doc = Document(self._store, self._collection, self._id)
                # DocumentReferenceオブジェクトを作成
                self._reference = DocumentReference(doc)
        return self._reference
    
    # DocumentSnapshotクラスに新しいメソッドとプロパティを追加
    DocumentSnapshot.__init__ = new_init
    DocumentSnapshot.reference = property(reference_property)
    
    # Document.getメソッドを修正して、collection名とstoreオブジェクトを渡すようにする
    from storekiss.crud import Document
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

def test_firestore_compatible_patch():
    """
    Firestoreと互換性のあるパッチをテストします。
    """
    # パッチを適用
    apply_firestore_compatible_patch()
    
    # データベースファイルのパス
    db_path = "firestore_compatible_test.db"
    
    # 既存のファイルがあれば削除
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # クライアントを作成
    db = litestore.Client(db_path)
    
    # コレクション名
    collection_name = 'test_firestore_compatible'
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
    
    # Firestoreと同じ構文で更新: doc.reference.update()
    logger.info("\nFirestoreと同じ構文で更新: doc.reference.update()")
    start_time = time.time()
    count = 0
    for doc in docs:
        # doc.reference.update()を使用して更新
        doc.reference.update({'check': True})
        count += 1
        logger.info("ドキュメント %s を更新しました (check=True)", doc.id)
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
    test_firestore_compatible_patch()
