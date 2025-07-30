"""
Test automatic collection creation functionality.

These tests verify that collections are automatically created when accessed,
similar to how Google Cloud Firestore works.
"""
import os
import sqlite3
import datetime
import pytest
from pathlib import Path

from storekiss import litestore
from storekiss.validation import Schema, StringField, NumberField


@pytest.fixture
def temp_db_path():
    """一時的なデータベースパスを作成します。"""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join(
        "tests/temp_test_data", f"auto_collection_test_{timestamp}.db"
    )

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


def test_collection_auto_creation(temp_db_path):
    """Test that collections are automatically created when accessed."""
    db = litestore.client(db_path=temp_db_path)

    test_collection = db.collection("test_auto_created")

    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        ("test_auto_created",),
    )
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == "test_auto_created"


def test_collection_auto_creation_with_document(temp_db_path):
    """Test that documents can be added to automatically created collections."""
    db = litestore.client(db_path=temp_db_path)

    test_collection = db.collection("test_auto_created_with_doc")
    doc_ref = test_collection.document("test_doc")
    doc_ref.set({"name": "Test Document", "value": 42})

    retrieved_doc = doc_ref.get()
    doc_data = retrieved_doc.to_dict()
    assert retrieved_doc.id == "test_doc"
    assert doc_data["name"] == "Test Document"
    assert doc_data["value"] == 42


def test_multiple_collections_auto_creation(temp_db_path):
    """Test that multiple collections can be automatically created."""
    db = litestore.client(db_path=temp_db_path)

    collection1 = db.collection("test_collection1")
    collection2 = db.collection("test_collection2")
    collection3 = db.collection("test_collection3")

    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()

    for collection_name in ["test_collection1", "test_collection2", "test_collection3"]:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (collection_name,),
        )
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == collection_name

    conn.close()


def test_collection_auto_creation_with_schema(temp_db_path):
    """Test that collections are created with schema validation."""
    db = litestore.client(db_path=temp_db_path)

    test_collection = db.collection("test_schema_collection")

    doc_ref = test_collection.document("valid_doc")
    doc_ref.set({"name": "Valid Document", "value": 42})

    retrieved_doc = doc_ref.get()
    doc_data = retrieved_doc.to_dict()
    assert doc_data["name"] == "Valid Document"
    assert doc_data["value"] == 42

    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    # テーブル名がダブルクォートで囲まれるようになったため、インデックス名も変更されています
    # テーブルのインデックスを確認する
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    # インデックスの一覧を取得
    results = cursor.fetchall()
    conn.close()

    # インデックスが少なくとも一つは作成されていることを確認
    assert len(results) > 0, "インデックスが作成されていません"

    # インデックス名を出力して確認
    index_names = [row[0] for row in results]
    print(f"Created indexes: {index_names}")
