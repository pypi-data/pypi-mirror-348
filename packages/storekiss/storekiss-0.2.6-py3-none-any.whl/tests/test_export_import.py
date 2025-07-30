"""
LiteStore互換エクスポート/インポート機能のテスト
"""
import os
import json
import tempfile
import shutil
import datetime
import pytest
from pathlib import Path

from storekiss.crud import LiteStore
# from storekiss.validation import Schema, StringField, NumberField, BooleanField
from storekiss.export_import import LiteStoreExporter, LiteStoreImporter


@pytest.fixture
def temp_db_path():
    """一時的なデータベースファイルのパスを返すフィクスチャ"""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join("tests/temp_test_data", f"export_import_test_{timestamp}.db")

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


@pytest.fixture
def temp_export_dir():
    """一時的なエクスポートディレクトリを作成します。"""
    # tests/temp_test_data ディレクトリに一時ディレクトリを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    export_dir = os.path.join("tests/temp_test_data", f"export_import_{timestamp}")
    os.makedirs(export_dir, exist_ok=True)

    yield export_dir

    # テスト後にディレクトリを削除しないようにして、データを保持
    # if os.path.exists(export_dir):
    #     shutil.rmtree(export_dir)


@pytest.fixture
def db_with_data(temp_db_path):
    """テスト用のデータを含むデータベースを作成します。"""
    # 都道府県用スキーマを定義
    # prefecture_schema = Schema(
    #     {
    #         "number": NumberField(required=True),
    #         "name": StringField(required=True),
    #         "active": BooleanField(required=False),
    #     },
    #     allow_extra_fields=True,
    # )

    # 都市用スキーマを定義
    # city_schema = Schema(
    #     {"name": StringField(required=True), "population": NumberField(required=True)},
    #     allow_extra_fields=True,
    # )

    # LiteStoreクライアントを作成
    db = LiteStore(db_path=temp_db_path)

    # 都道府県コレクションを作成
    prefectures = db.collection("都道府県")

    # いくつかの都道府県データを追加
    prefectures.document("hokkaido").set({"number": 1, "name": "北海道", "active": True})

    prefectures.document("tokyo").set({"number": 13, "name": "東京都", "active": True})

    prefectures.document("osaka").set({"number": 27, "name": "大阪府", "active": True})

    # 都市コレクションを作成（都市用スキーマを使用）
    cities = db.collection("cities")

    # いくつかの都市データを追加
    cities.document("tokyo").set({"name": "東京", "population": 13960000})

    cities.document("osaka").set({"name": "大阪", "population": 8839000})

    return db


class TestExportImport:
    """エクスポート/インポート機能のテストクラス"""

    def test_export_collection(self, db_with_data, temp_export_dir):
        """コレクションのエクスポート機能をテストします。"""
        # コレクションをエクスポート
        metadata_file = db_with_data.export_collection("都道府県", temp_export_dir)

        # メタデータファイルが作成されたことを確認
        assert os.path.exists(metadata_file)

        # メタデータファイルの内容を確認
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            assert "version" in metadata
            assert "exportTime" in metadata
            assert "collections" in metadata
            assert len(metadata["collections"]) == 1
            assert metadata["collections"][0]["name"] == "都道府県"
            assert metadata["collections"][0]["documentCount"] == 3

        # JSONLファイルが作成されたことを確認
        jsonl_file = os.path.join(temp_export_dir, "都道府県", "都道府県.jsonl")
        assert os.path.exists(jsonl_file)

        # JSONLファイルの内容を確認
        with open(jsonl_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 3

            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "hokkaido" in doc_ids
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids

            # フィールド形式を確認
            for doc in docs:
                assert "fields" in doc
                assert "createTime" in doc
                assert "updateTime" in doc

                # 特定のドキュメントの内容を確認
                if doc["name"].split("/")[-1] == "tokyo":
                    fields = doc["fields"]
                    assert "number" in fields
                    assert "integerValue" in fields["number"]
                    assert fields["number"]["integerValue"] == "13"

                    assert "name" in fields
                    assert "stringValue" in fields["name"]
                    assert fields["name"]["stringValue"] == "東京都"

                    assert "active" in fields
                    assert "integerValue" in fields["active"]
                    assert fields["active"]["integerValue"] == "True"

    def test_import_collection(self, db_with_data, temp_export_dir, temp_db_path):
        """コレクションのインポート機能をテストします。"""
        # コレクションをエクスポート
        db_with_data.export_collection("都道府県", temp_export_dir)

        # 新しいデータベースを作成
        # schema = Schema(
        #     {
        #         "number": NumberField(required=True),
        #         "name": StringField(required=True),
        #         "active": BooleanField(required=False),
        #     }
        # )

        new_db_path = temp_db_path + ".new"
        new_db = LiteStore(db_path=new_db_path)

        try:
            # エクスポートしたデータをインポート
            imported_count = new_db.import_collection("都道府県", temp_export_dir)

            # インポートされたドキュメント数を確認
            assert imported_count == 3

            # インポートされたデータを確認
            imported_docs = new_db.collection("都道府県").get()
            assert len(imported_docs) == 3

            # ドキュメントの内容を確認
            doc_ids = [doc.id for doc in imported_docs]
            assert "hokkaido" in doc_ids
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids

            # 特定のドキュメントの内容を確認
            for doc in imported_docs:
                doc_data = doc.to_dict()
                if doc.id == "tokyo":
                    assert doc_data["number"] == 13
                    assert doc_data["name"] == "東京都"
                    assert doc_data["active"] is True

        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)

    def test_export_all_collections(self, db_with_data, temp_export_dir):
        """すべてのコレクションのエクスポート機能をテストします。"""
        # すべてのコレクションをエクスポート
        metadata_file = db_with_data.export_all_collections(temp_export_dir)

        # メタデータファイルが作成されたことを確認
        assert os.path.exists(metadata_file)

        # メタデータファイルの内容を確認
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            assert "version" in metadata
            assert "exportTime" in metadata
            assert "collections" in metadata
            assert len(metadata["collections"]) == 2

            # コレクション名を確認
            collection_names = [c["name"] for c in metadata["collections"]]
            assert "都道府県" in collection_names
            assert "cities" in collection_names

            # ドキュメント数を確認
            for collection in metadata["collections"]:
                if collection["name"] == "都道府県":
                    assert collection["documentCount"] == 3
                elif collection["name"] == "cities":
                    assert collection["documentCount"] == 2

        # 各コレクションのJSONLファイルが作成されたことを確認
        pref_jsonl_file = os.path.join(temp_export_dir, "都道府県", "都道府県.jsonl")
        assert os.path.exists(pref_jsonl_file)

        cities_jsonl_file = os.path.join(temp_export_dir, "cities", "cities.jsonl")
        assert os.path.exists(cities_jsonl_file)

        # 都道府県コレクションのJSONLファイルの内容を確認
        with open(pref_jsonl_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 3

        # 都市コレクションのJSONLファイルの内容を確認
        with open(cities_jsonl_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 2

            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids

            # 特定のドキュメントの内容を確認
            for doc in docs:
                if doc["name"].split("/")[-1] == "tokyo":
                    fields = doc["fields"]
                    assert "name" in fields
                    assert "stringValue" in fields["name"]
                    assert fields["name"]["stringValue"] == "東京"

                    assert "population" in fields
                    assert "integerValue" in fields["population"]
                    assert fields["population"]["integerValue"] == "13960000"

    def test_import_all_collections(self, db_with_data, temp_export_dir, temp_db_path):
        """すべてのコレクションのインポート機能をテストします。"""
        # すべてのコレクションをエクスポート
        db_with_data.export_all_collections(temp_export_dir)

        # 新しいデータベースを作成
        # schema = Schema(
        #     {
        #         "number": NumberField(required=True),
        #         "name": StringField(required=True),
        #         "active": BooleanField(required=False),
        #     }
        # )

        new_db_path = temp_db_path + ".new"
        new_db = LiteStore(db_path=new_db_path)

        try:
            # エクスポートしたデータをインポート
            import_result = new_db.import_all_collections(temp_export_dir)

            # インポート結果を確認
            assert "都道府県" in import_result
            assert "cities" in import_result
            assert import_result["都道府県"] == 3
            assert import_result["cities"] == 2

            # インポートされたデータを確認（都道府県コレクション）
            pref_docs = new_db.collection("都道府県").get()
            assert len(pref_docs) == 3

            # インポートされたデータを確認（都市コレクション）
            city_docs = new_db.collection("cities").get()
            assert len(city_docs) == 2

            # 都市コレクションの内容を確認
            for doc in city_docs:
                doc_data = doc.to_dict()
                if doc.id == "tokyo":
                    assert doc_data["name"] == "東京"
                    assert doc_data["population"] == 13960000

        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)

    def test_litestore_field_conversion(self, db_with_data, temp_export_dir):
        """LiteStoreフィールド変換機能をテストします。"""
        # 複雑なデータを含むドキュメントを作成
        complex_data = db_with_data.collection("complex_data")
        complex_data.document("test1").set(
            {
                "string": "文字列",
                "integer": 42,
                "float": 3.14,
                "boolean": True,
                "null": None,
                "array": [1, "文字列", True, None],
                "map": {"key1": "値1", "key2": 123, "nested": {"inner": "内部値"}},
            }
        )

        # コレクションをエクスポート
        db_with_data.export_collection("complex_data", temp_export_dir)

        # JSONLファイルの内容を確認
        jsonl_file = os.path.join(temp_export_dir, "complex_data", "complex_data.jsonl")
        assert os.path.exists(jsonl_file)

        with open(jsonl_file, "r", encoding="utf-8") as f:
            doc = json.loads(f.readline())
            fields = doc["fields"]

            # 基本型の変換を確認
            assert "stringValue" in fields["string"]
            assert fields["string"]["stringValue"] == "文字列"

            assert "integerValue" in fields["integer"]
            assert fields["integer"]["integerValue"] == "42"

            assert "doubleValue" in fields["float"]
            assert fields["float"]["doubleValue"] == 3.14

            assert "integerValue" in fields["boolean"]
            assert fields["boolean"]["integerValue"] == "True"

            assert "nullValue" in fields["null"]
            assert fields["null"]["nullValue"] is None

            # 配列の変換を確認
            assert "arrayValue" in fields["array"]
            array_values = fields["array"]["arrayValue"]["values"]
            assert len(array_values) == 4
            assert "integerValue" in array_values[0]
            assert array_values[0]["integerValue"] == "1"
            assert "stringValue" in array_values[1]
            assert array_values[1]["stringValue"] == "文字列"
            assert "integerValue" in array_values[2]
            assert array_values[2]["integerValue"] == "True"
            assert "nullValue" in array_values[3]
            assert array_values[3]["nullValue"] is None

            # マップの変換を確認
            assert "mapValue" in fields["map"]
            map_fields = fields["map"]["mapValue"]["fields"]
            assert "stringValue" in map_fields["key1"]
            assert map_fields["key1"]["stringValue"] == "値1"
            assert "integerValue" in map_fields["key2"]
            assert map_fields["key2"]["integerValue"] == "123"
            assert "mapValue" in map_fields["nested"]
            assert "stringValue" in map_fields["nested"]["mapValue"]["fields"]["inner"]
            assert (
                map_fields["nested"]["mapValue"]["fields"]["inner"]["stringValue"]
                == "内部値"
            )

        # 新しいデータベースを作成
        # schema = Schema({})  # スキーマなし
        new_db_path = db_with_data.db_path + ".new"
        new_db = LiteStore(db_path=new_db_path)

        try:
            # エクスポートしたデータをインポート
            new_db.import_collection("complex_data", temp_export_dir)

            # インポートされたデータを確認
            imported_docs = new_db.collection("complex_data").get()
            assert len(imported_docs) == 1

            # 複雑なデータの内容を確認
            doc = imported_docs[0]
            doc_data = doc.to_dict()
            assert doc_data["string"] == "文字列"
            assert doc_data["integer"] == 42
            assert doc_data["float"] == 3.14
            assert doc_data["boolean"] is True
            assert doc_data["null"] is None
            assert doc_data["array"] == [1, "文字列", True, None]
            assert doc_data["map"]["key1"] == "値1"
            assert doc_data["map"]["key2"] == 123
            assert doc_data["map"]["nested"]["inner"] == "内部値"

        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)
