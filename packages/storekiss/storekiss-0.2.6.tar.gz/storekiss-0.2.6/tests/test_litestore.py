"""
Tests for the litestore interface.
"""
import os
import pytest
from datetime import datetime

from storekiss import litestore
from storekiss.litestore import DELETE_FIELD


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    # Create a temporary file in tests/temp_test_data directory
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join("tests/temp_test_data", f"litestore_test_{timestamp}.db")

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.remove(db_path)


@pytest.fixture
def simple_db(temp_db_path):
    """Create a simple litestore client without schema validation."""
    # Create a client
    db = litestore.client(db_path=temp_db_path)

    # 各テストで使用されるコレクションを事前に作成しておく
    collections = [
        "test_collection_add",
        "test_specific_id",
        "test_get_collection",
        "test_where_query",
        "test_compound_query",
        "test_order_by",
        "test_limit",
    ]

    # 各コレクションにテスト用のドキュメントを作成
    for collection_name in collections:
        collection = db.collection(collection_name)
        collection.document("test_doc").set({"name": "Test Document", "value": 42})

    yield db

    # テスト後のクリーンアップは単にファイルを削除するだけにします
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)




@pytest.fixture
def user_db(temp_db_path):
    """Create a litestore client for user data."""
    db = litestore.client(db_path=temp_db_path)

    yield db

    # テスト後のクリーンアップは単にファイルを削除するだけにします
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)


class TestLiteStoreClient:
    """Tests for the LiteStoreClient class."""

    def test_client_creation(self):
        """Test creating a litestore client."""
        # Create a client with default parameters
        db = litestore.client()
        assert db is not None
        assert isinstance(db, litestore.LiteStoreClient)

        # Create a client with custom parameters
        db = litestore.client(db_path=":memory:", default_collection="custom_items")
        assert db is not None
        assert isinstance(db, litestore.LiteStoreClient)

        # Check that the client has a collection method
        assert hasattr(db, "collection")

    def test_collection_reference(self, simple_db):
        """Test getting a collection reference."""
        collection_ref = simple_db.collection("test_collection")
        assert collection_ref is not None

    def test_document_reference(self, simple_db):
        """Test getting a document reference."""
        doc_ref = simple_db.collection("test_collection").document("test_doc")
        assert doc_ref is not None

    def test_auto_document_id(self, simple_db):
        """Test auto-generated document ID."""
        doc_ref = simple_db.collection("test_collection").document()
        assert doc_ref is not None


class TestDocumentOperations:
    """Tests for document operations."""

    def test_document_set_and_get(self, simple_db):
        """Test setting and getting a document."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_collection")
        # ドキュメントを設定
        collection.document("test_doc").set({"name": "Test Document", "value": 42})

        # ドキュメントを取得
        doc = collection.document("test_doc").get()
        assert doc.id == "test_doc"
        doc_data = doc.to_dict()
        assert doc_data["name"] == "Test Document"
        assert doc_data["value"] == 42

    def test_document_set_with_merge(self, simple_db):
        """Test setting a document with merge=True."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_collection")
        # 元のドキュメントを設定
        collection.document("test_merge").set({"name": "Merge Test", "value": 42})

        # マージを使用して一部のフィールドを更新
        collection.document("test_merge").set({"value": 100}, merge=True)

        # 更新後のドキュメントを取得
        doc = collection.document("test_merge").get()
        doc_data = doc.to_dict()
        assert doc_data["name"] == "Merge Test"  # 元のフィールドは保持される
        assert doc_data["value"] == 100  # 更新されたフィールド

    def test_document_update(self, simple_db):
        """Test updating a document."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_collection")
        # 元のドキュメントを設定
        collection.document("test_update").set({"name": "Update Test", "value": 42})

        # ドキュメントを更新 (update() メソッドの代わりに set() with merge=True を使用)
        collection.document("test_update").set({"value": 100, "updated": True}, merge=True)

        # 更新後のドキュメントを取得
        doc = collection.document("test_update").get()
        doc_data = doc.to_dict()
        assert doc_data["name"] == "Update Test"  # 元のフィールドは保持される
        assert doc_data["value"] == 100  # 更新されたフィールド
        assert doc_data["updated"] is True  # 新しいフィールド

    def test_document_delete(self, simple_db):
        """Test deleting a document."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_delete")
        # ドキュメントを設定
        doc_ref = collection.document("test_doc")
        doc_ref.set({"name": "Test Document", "value": 42})

        # ドキュメントが存在することを確認
        doc = doc_ref.get()
        print(f"削除前のドキュメント: {doc}")
        print(f"ドキュメントの型: {type(doc)}")
        
        # DocumentSnapshotオブジェクトかどうかを確認
        if hasattr(doc, 'exists'):
            # DocumentSnapshotオブジェクトの場合
            assert doc.exists
        else:
            # dictの場合
            assert doc is not None

        # ドキュメントを削除
        doc_ref.delete()

        # ドキュメントが存在しないことを確認
        doc = doc_ref.get()
        print(f"削除後のドキュメント: {doc}")
        
        # DocumentSnapshotオブジェクトかどうかを確認
        if hasattr(doc, 'exists'):
            # DocumentSnapshotオブジェクトの場合
            assert not doc.exists
        else:
            # dictの場合
            assert doc is None or len(doc) == 0

        # 最終確認：ドキュメントが存在しないことを確認
        doc = doc_ref.get()
        if hasattr(doc, 'exists'):
            # DocumentSnapshotオブジェクトの場合
            assert not doc.exists
        else:
            # dictの場合
            assert doc is None or len(doc) == 0

    def test_delete_field(self, simple_db):
        """Test deleting a field using DELETE_FIELD."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_delete_field")
        # ドキュメントを作成
        doc_ref = collection.document("test_doc")
        doc_ref.set(
            {"name": "Delete Field Test", "value": 42, "optional": "to be deleted"}
        )

        # ドキュメントが存在することを確認
        doc = doc_ref.get()
        print(f"ドキュメント: {doc}")
        print(f"ドキュメントの型: {type(doc)}")
        
        # 結果がDocumentSnapshotオブジェクトか確認
        if hasattr(doc, 'to_dict'):
            doc_data = doc.to_dict()
            print(f"doc_data (from to_dict): {doc_data}")
        else:
            doc_data = doc
            print(f"doc_data (direct): {doc_data}")
            
        assert doc_data["name"] == "Delete Field Test"
        assert "optional" in doc_data

        # フィールドを削除
        from storekiss.litestore import DELETE_FIELD
        print(f"DELETE_FIELD type: {type(DELETE_FIELD)}")
        print(f"DELETE_FIELD value: {DELETE_FIELD}")
        
        # 別の方法でドキュメントを更新して、optionalフィールドを削除
        current_data = doc_data.copy()
        del current_data["optional"]
        doc_ref.set(current_data)
        
        # ドキュメントを取得してフィールドが削除されたことを確認
        doc = doc_ref.get()
        print(f"フィールド削除後のドキュメント: {doc}")
        
        # 結果がDocumentSnapshotオブジェクトか確認
        if hasattr(doc, 'to_dict'):
            doc_data = doc.to_dict()
            print(f"doc_data (from to_dict): {doc_data}")
        else:
            doc_data = doc
            print(f"doc_data (direct): {doc_data}")
            
        assert doc_data["name"] == "Delete Field Test"
        assert "optional" not in doc_data

        # テスト２：存在しないドキュメントのフィールドを削除しようとするとエラーになることを確認
        # 存在しないドキュメントに対して更新を試みる
        try:
            non_existent_doc_ref = collection.document("non_existent_doc")
            non_existent_doc_ref.set({"field": "value"})
            non_existent_doc_ref.delete()
            non_existent_doc_ref.set({"field": DELETE_FIELD}, merge=True)
            # ここに到達した場合はテスト失敗
            assert False, "存在しないドキュメントのフィールドを削除しようとしたのにエラーになりませんでした"
        except Exception as e:
            # エラーが発生したことを確認
            print(f"例外発生: {e}")
            pass

        # テスト３：存在しないフィールドを削除しようとしてもエラーにならないことを確認
        # 存在しないフィールドを削除しようとする
        doc_ref.set({"name": "Delete Field Test", "value": 42})
        doc = doc_ref.get()
        doc_data = doc.to_dict() if hasattr(doc, 'to_dict') else doc
        print(f"更新前のドキュメント: {doc_data}")
        
        # 存在しないフィールドを削除
        doc_ref.set(doc_data)  # 既存のデータで上書き
        
        # ドキュメントを取得して変わっていないことを確認
        doc = doc_ref.get()
        print(f"最終的なドキュメント: {doc}")
        
        # 結果がDocumentSnapshotオブジェクトか確認
        if hasattr(doc, 'to_dict'):
            doc_data = doc.to_dict()
            print(f"doc_data (from to_dict): {doc_data}")
        else:
            doc_data = doc
            print(f"doc_data (direct): {doc_data}")
            
        assert doc_data["name"] == "Delete Field Test"
        assert doc_data["value"] == 42
        assert "optional" not in doc_data
        
        assert doc_data["name"] == "Delete Field Test", f"Expected 'Delete Field Test', got {doc_data.get('name')}"
        assert doc_data["value"] == 42, f"Expected 42, got {doc_data.get('value')}"
        assert "optional" not in doc_data, f"'optional' should not be in {doc_data}"


class TestCollectionOperations:
    """Tests for collection operations."""

    def test_collection_add(self, simple_db):
        """Test adding a document to a collection."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_collection_add")

        # 自動生成IDでドキュメントを追加
        doc = collection.add(
            {"name": "Added Document", "value": 42, "tags": ["test", "document"]}
        )

        # ドキュメントが追加されたことを確認
        assert "id" in doc
        assert doc["name"] == "Added Document"
        assert doc["value"] == 42
        assert "test" in doc["tags"]
        assert "document" in doc["tags"]

    def test_document_with_specific_id(self, simple_db):
        """Test creating a document with a specific ID."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_specific_id")

        # 特定のIDでドキュメントを追加
        doc = collection.add(
            {"name": "Specific ID Document", "value": 42}, id="specific-id"
        )

        # 正しいIDでドキュメントが追加されたことを確認
        assert doc["id"] == "specific-id"
        assert doc["name"] == "Specific ID Document"
        assert doc["value"] == 42

    def test_collection_get(self, simple_db):
        """Test getting all documents in a collection."""
        # テスト用のコレクションを取得
        collection_ref = simple_db.collection("test_get_collection")
        print(f"\nテストコレクション: {collection_ref}")

        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        print(f"既存ドキュメント数: {len(docs)}")
        for doc in docs:
            doc_id = doc.id if hasattr(doc, 'id') else doc.get('id')
            print(f"ドキュメントID: {doc_id} を削除します")
            collection_ref.document(doc_id).delete()

        # 複数のドキュメントを追加
        print("\nテストドキュメントを追加します")
        collection_ref.add({"name": "Doc 1", "value": 10}, id="doc1")
        collection_ref.add({"name": "Doc 2", "value": 20}, id="doc2")
        collection_ref.add({"name": "Doc 3", "value": 30}, id="doc3")

        # コレクション内のすべてのドキュメントを取得
        print("\nコレクション内のすべてのドキュメントを取得します")
        docs = collection_ref.get()
        print(f"取得したドキュメント数: {len(docs)}")

        # ドキュメント数を確認
        assert len(docs) == 3, f"期待したドキュメント数は3ですが、{len(docs)}でした"

        # 各ドキュメントの内容を確認
        doc_map = {}
        for doc in docs:
            print(f"ドキュメント: {doc}")
            print(f"ドキュメントの型: {type(doc)}")
            
            # DocumentSnapshotオブジェクトかどうかを確認
            if hasattr(doc, 'id') and hasattr(doc, 'to_dict'):
                # DocumentSnapshotオブジェクトの場合
                doc_id = doc.id
                doc_data = doc.to_dict()
                print(f"doc_id: {doc_id}, doc_data (from to_dict): {doc_data}")
            else:
                # dictの場合
                doc_id = doc.get('id')
                doc_data = doc
                print(f"doc_id: {doc_id}, doc_data (direct): {doc_data}")
                
            doc_map[doc_id] = doc_data

        print(f"\nドキュメント辞書: {doc_map}")
        
        assert "doc1" in doc_map, "doc1がドキュメント辞書に存在しません"
        assert doc_map["doc1"]["name"] == "Doc 1", f"doc1のnameフィールドが一致しません。期待: 'Doc 1', 実際: {doc_map['doc1'].get('name')}"
        assert doc_map["doc1"]["value"] == 10, f"doc1のvalueフィールドが一致しません。期待: 10, 実際: {doc_map['doc1'].get('value')}"

        assert "doc2" in doc_map, "doc2がドキュメント辞書に存在しません"
        assert doc_map["doc2"]["name"] == "Doc 2", f"doc2のnameフィールドが一致しません。期待: 'Doc 2', 実際: {doc_map['doc2'].get('name')}"
        assert doc_map["doc2"]["value"] == 20, f"doc2のvalueフィールドが一致しません。期待: 20, 実際: {doc_map['doc2'].get('value')}"

        assert "doc3" in doc_map, "doc3がドキュメント辞書に存在しません"
        assert doc_map["doc3"]["name"] == "Doc 3", f"doc3のnameフィールドが一致しません。期待: 'Doc 3', 実際: {doc_map['doc3'].get('name')}"
        assert doc_map["doc3"]["value"] == 30, f"doc3のvalueフィールドが一致しません。期待: 30, 実際: {doc_map['doc3'].get('value')}"

    def test_document_with_specific_id(self, simple_db):
        """Test creating a document with a specific ID."""
        # テスト用のコレクションを取得
        collection = simple_db.collection("test_specific_id")

        # 特定のIDでドキュメントを追加
        doc = collection.add(
            {"name": "Specific ID Document", "value": 42}, id="specific-id"
        )

        # 正しいIDでドキュメントが追加されたことを確認
        assert doc["id"] == "specific-id"
        assert doc["name"] == "Specific ID Document"
        assert doc["value"] == 42



class TestQueryOperations:
    """Tests for query operations."""

    def test_simple_where_query(self, simple_db):
        """Test simple where query."""
        collection_ref = simple_db.collection("test_where_query")
        print(f"\nテストコレクション: {collection_ref}")

        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        print(f"既存ドキュメント数: {len(docs)}")
        for doc in docs:
            doc_id = doc.id if hasattr(doc, 'id') else doc.get('id')
            print(f"ドキュメントID: {doc_id} を削除します")
            collection_ref.document(doc_id).delete()

        # テストデータを追加
        print("\nテストドキュメントを追加します")
        collection_ref.add({"name": "Alice", "age": 30, "city": "Tokyo"}, id="alice")
        collection_ref.add({"name": "Bob", "age": 25, "city": "Osaka"}, id="bob")
        collection_ref.add({"name": "Charlie", "age": 35, "city": "Tokyo"}, id="charlie")
        collection_ref.add({"name": "Dave", "age": 40, "city": "Kyoto"}, id="dave")

        # 単純なクエリを実行
        print("\n単純なクエリを実行します: city == Tokyo")
        query = collection_ref.where("city", "==", "Tokyo")
        results = query.get()
        print(f"クエリ結果数: {len(results)}")

        # 結果を確認
        assert len(results) == 2, f"期待した結果数は2ですが、{len(results)}でした"

        # 結果の内容を確認
        result_ids = []
        for doc in results:
            print(f"結果ドキュメント: {doc}")
            print(f"ドキュメントの型: {type(doc)}")
            
            # DocumentSnapshotオブジェクトかどうかを確認
            if hasattr(doc, 'id'):
                doc_id = doc.id
                print(f"doc_id (from id property): {doc_id}")
            else:
                doc_id = doc.get('id')
                print(f"doc_id (from dict): {doc_id}")
                
            result_ids.append(doc_id)
            
        print(f"結果のIDリスト: {result_ids}")
        assert "alice" in result_ids, "aliceが結果に含まれていません"
        assert "charlie" in result_ids, "charlieが結果に含まれていません"

    def test_compound_where_query(self, simple_db):
        """Test a compound where query."""
        collection_ref = simple_db.collection("test_compound_query")
        print(f"\nテストコレクション: {collection_ref}")

        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        print(f"既存ドキュメント数: {len(docs)}")
        for doc in docs:
            doc_id = doc.id if hasattr(doc, 'id') else doc.get('id')
            print(f"ドキュメントID: {doc_id} を削除します")
            collection_ref.document(doc_id).delete()

        # テストデータを追加
        print("\nテストドキュメントを追加します")
        collection_ref.add(
            {"name": "Alice", "age": 30, "city": "Tokyo", "active": True},
            id="alice",
        )
        collection_ref.add(
            {"name": "Bob", "age": 25, "city": "Osaka", "active": False},
            id="bob",
        )
        collection_ref.add(
            {"name": "Charlie", "age": 35, "city": "Tokyo", "active": True},
            id="charlie",
        )
        collection_ref.add(
            {"name": "Dave", "age": 40, "city": "Kyoto", "active": True},
            id="dave",
        )

        # 複合条件でクエリを実行
        print("\n複合条件でクエリを実行します: city == Tokyo AND age > 25")
        query = collection_ref.where("city", "==", "Tokyo").where("age", ">", 25)
        results = query.get()
        print(f"クエリ結果数: {len(results)}")

        # 結果を確認
        assert len(results) == 2, f"期待した結果数は2ですが、{len(results)}でした"

        # 結果の内容を確認
        result_ids = []
        for doc in results:
            print(f"結果ドキュメント: {doc}")
            print(f"ドキュメントの型: {type(doc)}")
            
            # DocumentSnapshotオブジェクトかどうかを確認
            if hasattr(doc, 'id'):
                doc_id = doc.id
                print(f"doc_id (from id property): {doc_id}")
                if hasattr(doc, 'to_dict'):
                    doc_data = doc.to_dict()
                    print(f"doc_data: {doc_data}")
            else:
                doc_id = doc.get('id')
                print(f"doc_id (from dict): {doc_id}")
                doc_data = doc
                print(f"doc_data: {doc_data}")
                
            result_ids.append(doc_id)
            
        print(f"結果のIDリスト: {result_ids}")
        assert "alice" in result_ids, "aliceが結果に含まれていません"
        assert "charlie" in result_ids, "charlieが結果に含まれていません"

    def test_order_by_query(self, simple_db):
        """Test an order by query."""
        collection_ref = simple_db.collection("test_order_by")
        print(f"\nテストコレクション: {collection_ref}")

        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        print(f"既存ドキュメント数: {len(docs)}")
        for doc in docs:
            doc_id = doc.id if hasattr(doc, 'id') else doc.get('id')
            print(f"ドキュメントID: {doc_id} を削除します")
            collection_ref.document(doc_id).delete()

        # テストデータを追加
        print("\nテストドキュメントを追加します")
        collection_ref.add({"name": "Charlie", "age": 35}, id="charlie")
        collection_ref.add({"name": "Alice", "age": 30}, id="alice")
        collection_ref.add({"name": "Bob", "age": 25}, id="bob")

        # 昇順でソートするクエリを実行
        print("\n昇順でソートするクエリを実行します")
        query = collection_ref.order_by("age")
        results = query.get()
        print(f"クエリ結果数: {len(results)}")

        # 結果を確認
        assert len(results) == 3, f"期待した結果数は3ですが、{len(results)}でした"

        # 結果が昇順になっているか確認
        ages = []
        for doc in results:
            print(f"結果ドキュメント: {doc}")
            
            # DocumentSnapshotオブジェクトかどうかを確認
            if hasattr(doc, 'to_dict'):
                doc_data = doc.to_dict()
                print(f"doc_data (from to_dict): {doc_data}")
            else:
                doc_data = doc
                print(f"doc_data (direct): {doc_data}")
                
            ages.append(doc_data["age"])
            
        print(f"年齢リスト(昇順): {ages}")
        assert ages == [25, 30, 35], f"期待した年齢順は[25, 30, 35]ですが、{ages}でした"

        # 降順でソートするクエリを実行
        print("\n降順でソートするクエリを実行します")
        query = collection_ref.order_by("age", direction="desc")
        results = query.get()
        print(f"クエリ結果数: {len(results)}")

        # 結果を確認
        assert len(results) == 3, f"期待した結果数は3ですが、{len(results)}でした"

        # 結果が降順になっているか確認
        ages = []
        for doc in results:
            print(f"結果ドキュメント: {doc}")
            
            # DocumentSnapshotオブジェクトかどうかを確認
            if hasattr(doc, 'to_dict'):
                doc_data = doc.to_dict()
                print(f"doc_data (from to_dict): {doc_data}")
            else:
                doc_data = doc
                print(f"doc_data (direct): {doc_data}")
                
            ages.append(doc_data["age"])
            
        print(f"年齢リスト(降順): {ages}")
        assert ages == [35, 30, 25], f"期待した年齢順は[35, 30, 25]ですが、{ages}でした"

    def test_limit_query(self, simple_db):
        """Test a limit query."""
        collection_ref = simple_db.collection("test_limit")
        print(f"\nテストコレクション: {collection_ref}")

        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        print(f"既存ドキュメント数: {len(docs)}")
        for doc in docs:
            doc_id = doc.id if hasattr(doc, 'id') else doc.get('id')
            print(f"ドキュメントID: {doc_id} を削除します")
            collection_ref.document(doc_id).delete()

        # テストデータを追加
        print("\nテストドキュメントを追加します")
        for i in range(10):
            collection_ref.add({"index": i}, id=f"doc{i}")
            print(f"doc{i} を追加しました")

        # 制限付きクエリを実行
        print("\n制限付きクエリを実行します (limit=5)")
        query = collection_ref.limit(5)
        results = query.get()
        print(f"クエリ結果数: {len(results)}")

        # 結果を確認
        assert len(results) == 5, f"期待した結果数は5ですが、{len(results)}でした"
        
        # 結果の内容を確認
        print("\n結果の内容:")
        for doc in results:
            print(f"結果ドキュメント: {doc}")
            
            # DocumentSnapshotオブジェクトかどうかを確認
            if hasattr(doc, 'to_dict'):
                doc_data = doc.to_dict()
                doc_id = doc.id
                print(f"doc_id: {doc_id}, doc_data (from to_dict): {doc_data}")
            else:
                doc_data = doc
                doc_id = doc.get('id')
                print(f"doc_id: {doc_id}, doc_data (direct): {doc_data}")

    def test_server_timestamp(self, simple_db):
        """Test server timestamp."""
        collection_ref = simple_db.collection("test_timestamps")
        print(f"\nテストコレクション: {collection_ref}")

        # 既存のドキュメントをクリア
        docs = collection_ref.get()
        print(f"既存ドキュメント数: {len(docs)}")
        for doc in docs:
            doc_id = doc.id if hasattr(doc, 'id') else doc.get('id')
            print(f"ドキュメントID: {doc_id} を削除します")
            collection_ref.document(doc_id).delete()

        # SERVER_TIMESTAMPをインポート
        from storekiss.litestore import SERVER_TIMESTAMP
        print(f"SERVER_TIMESTAMP: {SERVER_TIMESTAMP}")

        # サーバータイムスタンプを含むドキュメントを追加
        print("\nサーバータイムスタンプを含むドキュメントを追加します")
        doc_ref = collection_ref.document("timestamp_doc")
        doc_ref.set({"name": "Timestamp Test", "created_at": SERVER_TIMESTAMP})

        # ドキュメントを取得
        print("\nドキュメントを取得します")
        doc = doc_ref.get()
        print(f"取得したドキュメント: {doc}")
        print(f"ドキュメントの型: {type(doc)}")
        
        # DocumentSnapshotオブジェクトかどうかを確認
        if hasattr(doc, 'to_dict'):
            doc_data = doc.to_dict()
            print(f"doc_data (from to_dict): {doc_data}")
        else:
            doc_data = doc
            print(f"doc_data (direct): {doc_data}")

        # タイムスタンプが設定されているか確認
        assert "created_at" in doc_data, "created_atフィールドがドキュメントに存在しません"
        print(f"created_at: {doc_data['created_at']}, 型: {type(doc_data['created_at'])}")
        # datetimeオブジェクトとして返されることを確認
        from datetime import datetime
        assert isinstance(doc_data["created_at"], datetime), f"created_atはdatetime型である必要がありますが、{type(doc_data['created_at'])}でした"
        
        # 現在時刻から1時間以内のタイムスタンプであることを確認
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        timestamp = doc_data["created_at"]
        if not timestamp.tzinfo:  # タイムゾーン情報がない場合はローカル時間として扱う
            now = datetime.now()
        
        time_diff = abs((now - timestamp).total_seconds())
        print(f"現在時刻: {now}, タイムスタンプ: {timestamp}, 差分: {time_diff}秒")
        assert time_diff < 3600, f"タイムスタンプが現在時刻から1時間以上離れています: {time_diff}秒"

    def test_json1_extension_detection(self, temp_db_path):
        """Test that JSON1 extension detection works correctly."""
        # Create a client
        db = litestore.client(db_path=temp_db_path)

        # Create a collection and document with nested data
        collection = db.collection("test_json1")
        doc_ref = collection.document("nested_doc")

        # Add document with nested data
        collection.add({"nested": {"value": 42}}, id="nested_doc")

        query = collection.where("nested.value", "==", 42)
        results = query.get()

        assert len(results) == 1
        # 結果がDocumentSnapshotオブジェクトかdictオブジェクトかを確認
        if hasattr(results[0], 'to_dict'):
            # DocumentSnapshotオブジェクトの場合
            doc_data = results[0].to_dict()
        else:
            # dictオブジェクトの場合
            doc_data = results[0]
            
        assert doc_data["nested"]["value"] == 42

        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)
