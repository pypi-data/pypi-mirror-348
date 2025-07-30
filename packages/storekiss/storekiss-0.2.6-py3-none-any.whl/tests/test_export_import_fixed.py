"""
LiteStore互換エクスポート/インポート機能のテスト
"""
import os
import json
import datetime
import pytest

from storekiss.crud import LiteStore
from storekiss.validation import Schema, StringField, NumberField, BooleanField
# 必要なインポートのみを残す
from storekiss.export_import import LiteStoreExporter


@pytest.fixture
def db_path_fixture():
    """一時的なデータベースパスを作成します。"""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join(
        "tests/temp_test_data", f"export_import_fixed_test_{timestamp}.db"
    )

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


@pytest.fixture
def export_dir_fixture():
    """一時的なエクスポートディレクトリを作成します。"""
    # tests/temp_test_data ディレクトリに一時ディレクトリを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    export_dir = os.path.join(
        "tests/temp_test_data", f"export_import_fixed_{timestamp}"
    )
    os.makedirs(export_dir, exist_ok=True)

    yield export_dir

    # テスト後にディレクトリを削除しないようにして、データを保持
    # if os.path.exists(export_dir):
    #     shutil.rmtree(export_dir)


@pytest.fixture
def db_fixture(db_path_fixture):
    """テスト用のデータを含むデータベースを作成します。"""
    # 都道府県用スキーマを定義
    prefecture_schema = Schema(
        {
            "number": NumberField(required=True),
            "name": StringField(required=True),
            "active": BooleanField(required=False),
        },
        allow_extra_fields=True,
    )

    # 都市用スキーマを定義
    city_schema = Schema(
        {"name": StringField(required=True), "population": NumberField(required=True)},
        allow_extra_fields=True,
    )

    # LiteStoreクライアントを作成
    db = LiteStore(db_path=db_path_fixture)

    # 都道府県コレクションを作成
    prefectures = db.collection("都道府県")
    # 注: 現在のLiteStoreクラスの実装ではschemaパラメータを受け付けていません

    # いくつかの都道府県データを追加
    prefectures.document("hokkaido").set({"number": 1, "name": "北海道", "active": True})

    prefectures.document("tokyo").set({"number": 13, "name": "東京都", "active": True})

    prefectures.document("osaka").set({"number": 27, "name": "大阪府", "active": True})

    # 都市コレクションを作成
    cities = db.collection("cities")
    # 注: 現在のLiteStoreクラスの実装ではschemaパラメータを受け付けていません

    # いくつかの都市データを追加
    cities.document("tokyo").set({"name": "東京", "population": 13960000})

    cities.document("osaka").set({"name": "大阪", "population": 8839000})

    return db


class TestExportImport:
    """エクスポート/インポート機能のテストクラス"""

    def test_export_import_basic(self, db_fixture, export_dir_fixture):
        """コレクションのエクスポート機能をテストします。"""
        # コレクションをエクスポート
        metadata_file = db_fixture.export_collection("都道府県", export_dir_fixture)

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
        jsonl_file = os.path.join(export_dir_fixture, "都道府県", "都道府県.jsonl")
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

    def test_export_import_with_schema(
        self, db_fixture, export_dir_fixture, db_path_fixture
    ):
        """コレクションのインポート機能をテストします。"""
        print("\n=== test_export_import_with_schema テスト開始 ===\n")
        
        # コレクションをエクスポート
        print("都道府県コレクションをエクスポートします")
        metadata_file = db_fixture.export_collection("都道府県", export_dir_fixture)

        # メタデータファイルが作成されたことを確認
        print(f"\nメタデータファイルの確認: {metadata_file}")
        assert os.path.exists(metadata_file), f"メタデータファイルが存在しません: {metadata_file}"

        # 新しいデータベースを作成
        schema = Schema(
            {
                "number": NumberField(required=True),
                "name": StringField(required=True),
                "active": BooleanField(required=False),
            },
            allow_extra_fields=True,
        )

        new_db_path = db_path_fixture + ".new"
        print(f"\n新しいデータベースを作成します: {new_db_path}")
        new_db = LiteStore(db_path=new_db_path)

        try:
            # エクスポートしたデータをインポート
            print("\nエクスポートしたデータをインポートします")
            imported_count = new_db.import_collection("都道府県", export_dir_fixture)
            print(f"インポートされたドキュメント数: {imported_count}")

            # インポートされたドキュメント数を確認
            assert imported_count == 3, f"インポートされたドキュメント数が一致しません。期待: 3, 実際: {imported_count}"

            # インポートされたデータを確認
            print("\nインポートされたデータを確認します")
            
            # 個別のドキュメントを直接取得する
            print("\n個別のドキュメントを取得します")
            collection = new_db.collection("都道府県")
            
            # hokkaidoドキュメントを取得
            print("hokkaidoドキュメントを取得します")
            hokkaido = collection.document("hokkaido").get()
            print(f"hokkaidoの型: {type(hokkaido)}")
            print(f"hokkaidoのhasattr(to_dict): {hasattr(hokkaido, 'to_dict')}")
            
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(hokkaido, 'to_dict'):
                hokkaido_data = hokkaido.to_dict()
                print(f"hokkaido_data (from to_dict): {hokkaido_data}")
            else:
                hokkaido_data = hokkaido
                print(f"hokkaido_data (direct): {hokkaido_data}")
                
            assert hokkaido_data is not None, "hokkaido_dataがNoneです"
            assert "number" in hokkaido_data, f"'number'フィールドがhokkaido_dataに存在しません: {hokkaido_data}"
            assert hokkaido_data["number"] == 1, f"hokkaidoのnumberフィールドが一致しません。期待: 1, 実際: {hokkaido_data.get('number')}"
            assert "name" in hokkaido_data, f"'name'フィールドがhokkaido_dataに存在しません: {hokkaido_data}"
            assert hokkaido_data["name"] == "北海道", f"hokkaidoのnameフィールドが一致しません。期待: '北海道', 実際: {hokkaido_data.get('name')}"
            
            # tokyoドキュメントを取得
            print("\ntokyoドキュメントを取得します")
            tokyo = collection.document("tokyo").get()
            print(f"tokyoの型: {type(tokyo)}")
            print(f"tokyoのhasattr(to_dict): {hasattr(tokyo, 'to_dict')}")
            
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(tokyo, 'to_dict'):
                tokyo_data = tokyo.to_dict()
                print(f"tokyo_data (from to_dict): {tokyo_data}")
            else:
                tokyo_data = tokyo
                print(f"tokyo_data (direct): {tokyo_data}")
                
            assert tokyo_data is not None, "tokyo_dataがNoneです"
            assert "number" in tokyo_data, f"'number'フィールドがtokyo_dataに存在しません: {tokyo_data}"
            assert tokyo_data["number"] == 13, f"tokyoのnumberフィールドが一致しません。期待: 13, 実際: {tokyo_data.get('number')}"
            assert "name" in tokyo_data, f"'name'フィールドがtokyo_dataに存在しません: {tokyo_data}"
            assert tokyo_data["name"] == "東京都", f"tokyoのnameフィールドが一致しません。期待: '東京都', 実際: {tokyo_data.get('name')}"
            
            # osakaドキュメントを取得
            print("\nosakaドキュメントを取得します")
            osaka = collection.document("osaka").get()
            print(f"osakaの型: {type(osaka)}")
            print(f"osakaのhasattr(to_dict): {hasattr(osaka, 'to_dict')}")
            
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(osaka, 'to_dict'):
                osaka_data = osaka.to_dict()
                print(f"osaka_data (from to_dict): {osaka_data}")
            else:
                osaka_data = osaka
                print(f"osaka_data (direct): {osaka_data}")
                
            assert osaka_data is not None, "osaka_dataがNoneです"
            assert "number" in osaka_data, f"'number'フィールドがosaka_dataに存在しません: {osaka_data}"
            assert osaka_data["number"] == 27, f"osakaのnumberフィールドが一致しません。期待: 27, 実際: {osaka_data.get('number')}"
            assert "name" in osaka_data, f"'name'フィールドがosaka_dataに存在しません: {osaka_data}"
            assert osaka_data["name"] == "大阪府", f"osakaのnameフィールドが一致しません。期待: '大阪府', 実際: {osaka_data.get('name')}"
            
            print("\n=== test_export_import_with_schema テスト成功 ===\n")


        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)

    def test_export_import_collection_filter(self, db_fixture, export_dir_fixture):
        """すべてのコレクションのエクスポート機能をテストします。"""
        # すべてのコレクションをエクスポート
        metadata_file = db_fixture.export_all_collections(export_dir_fixture)

        # メタデータファイルが作成されたことを確認
        assert os.path.exists(metadata_file)

        # メタデータファイルの内容を確認
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            assert "version" in metadata
            assert "exportTime" in metadata
            assert "collections" in metadata
            assert len(metadata["collections"]) == 2

            # コレクション名とドキュメント数を確認
            collection_info = {
                c["name"]: c["documentCount"] for c in metadata["collections"]
            }
            assert "都道府県" in collection_info
            assert "cities" in collection_info
            assert collection_info["都道府県"] == 3
            assert collection_info["cities"] == 2

        # 都道府県コレクションのJSONLファイルが作成されたことを確認
        prefecture_jsonl_file = os.path.join(export_dir_fixture, "都道府県", "都道府県.jsonl")
        assert os.path.exists(prefecture_jsonl_file)

        # 都市コレクションのJSONLファイルが作成されたことを確認
        city_jsonl_file = os.path.join(export_dir_fixture, "cities", "cities.jsonl")
        assert os.path.exists(city_jsonl_file)

        # 都道府県コレクションのJSONLファイルの内容を確認
        with open(prefecture_jsonl_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 3

            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "hokkaido" in doc_ids
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids

        # 都市コレクションのJSONLファイルの内容を確認
        with open(city_jsonl_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 2

            # 各ドキュメントの内容を確認
            docs = [json.loads(line) for line in lines]
            doc_ids = [doc["name"].split("/")[-1] for doc in docs]
            assert "tokyo" in doc_ids
            assert "osaka" in doc_ids

    def test_import_all_collections(
        self, db_fixture, export_dir_fixture, db_path_fixture
    ):
        """すべてのコレクションのインポート機能をテストします。"""
        print("\n=== test_import_all_collections テスト開始 ===\n")
        
        # すべてのコレクションをエクスポート
        print("すべてのコレクションをエクスポートします")
        metadata_file = db_fixture.export_all_collections(export_dir_fixture)

        # メタデータファイルが作成されたことを確認
        print(f"\nメタデータファイルの確認: {metadata_file}")
        assert os.path.exists(metadata_file), f"メタデータファイルが存在しません: {metadata_file}"

        # 新しいデータベースを作成
        new_db_path = db_path_fixture + ".new"
        print(f"\n新しいデータベースを作成します: {new_db_path}")
        new_db = LiteStore(db_path=new_db_path)

        try:
            # すべてのコレクションをインポート
            print("\nすべてのコレクションをインポートします")
            result = new_db.import_all_collections(export_dir_fixture)
            print(f"インポート結果: {result}")

            # 都道府県コレクションのデータを確認
            print("\n都道府県コレクションのデータを確認します")
            prefectures = new_db.collection("都道府県")
            
            # 個別のドキュメントを取得
            print("hokkaidoドキュメントを取得します")
            hokkaido = prefectures.document("hokkaido").get()
            print(f"hokkaidoの型: {type(hokkaido)}")
            print(f"hokkaidoのhasattr(to_dict): {hasattr(hokkaido, 'to_dict')}")
            
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(hokkaido, 'to_dict'):
                hokkaido_data = hokkaido.to_dict()
                print(f"hokkaido_data (from to_dict): {hokkaido_data}")
            else:
                hokkaido_data = hokkaido
                print(f"hokkaido_data (direct): {hokkaido_data}")
                
            assert hokkaido_data is not None, "hokkaido_dataがNoneです"
            assert "number" in hokkaido_data, f"'number'フィールドがhokkaido_dataに存在しません: {hokkaido_data}"
            assert hokkaido_data["number"] == 1, f"hokkaidoのnumberフィールドが一致しません。期待: 1, 実際: {hokkaido_data.get('number')}"
            assert "name" in hokkaido_data, f"'name'フィールドがhokkaido_dataに存在しません: {hokkaido_data}"
            assert hokkaido_data["name"] == "北海道", f"hokkaidoのnameフィールドが一致しません。期待: '北海道', 実際: {hokkaido_data.get('name')}"
            assert "active" in hokkaido_data, f"'active'フィールドがhokkaido_dataに存在しません: {hokkaido_data}"
            assert hokkaido_data["active"] is True, f"hokkaidoのactiveフィールドが一致しません。期待: True, 実際: {hokkaido_data.get('active')}"

            print("\ntokyoドキュメントを取得します")
            tokyo = prefectures.document("tokyo").get()
            print(f"tokyoの型: {type(tokyo)}")
            print(f"tokyoのhasattr(to_dict): {hasattr(tokyo, 'to_dict')}")
            
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(tokyo, 'to_dict'):
                tokyo_data = tokyo.to_dict()
                print(f"tokyo_data (from to_dict): {tokyo_data}")
            else:
                tokyo_data = tokyo
                print(f"tokyo_data (direct): {tokyo_data}")
                
            assert tokyo_data is not None, "tokyo_dataがNoneです"
            assert "number" in tokyo_data, f"'number'フィールドがtokyo_dataに存在しません: {tokyo_data}"
            assert tokyo_data["number"] == 13, f"tokyoのnumberフィールドが一致しません。期待: 13, 実際: {tokyo_data.get('number')}"
            assert "name" in tokyo_data, f"'name'フィールドがtokyo_dataに存在しません: {tokyo_data}"
            assert tokyo_data["name"] == "東京都", f"tokyoのnameフィールドが一致しません。期待: '東京都', 実際: {tokyo_data.get('name')}"
            assert "active" in tokyo_data, f"'active'フィールドがtokyo_dataに存在しません: {tokyo_data}"
            assert tokyo_data["active"] is True, f"tokyoのactiveフィールドが一致しません。期待: True, 実際: {tokyo_data.get('active')}"

            # 都市コレクションのデータを確認
            print("\n都市コレクションのデータを確認します")
            cities = new_db.collection("cities")
            
            print("tokyo_cityドキュメントを取得します")
            tokyo_city = cities.document("tokyo").get()
            print(f"tokyo_cityの型: {type(tokyo_city)}")
            print(f"tokyo_cityのhasattr(to_dict): {hasattr(tokyo_city, 'to_dict')}")
            
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(tokyo_city, 'to_dict'):
                tokyo_city_data = tokyo_city.to_dict()
                print(f"tokyo_city_data (from to_dict): {tokyo_city_data}")
            else:
                tokyo_city_data = tokyo_city
                print(f"tokyo_city_data (direct): {tokyo_city_data}")
                
            assert tokyo_city_data is not None, "tokyo_city_dataがNoneです"
            assert "name" in tokyo_city_data, f"'name'フィールドがtokyo_city_dataに存在しません: {tokyo_city_data}"
            assert tokyo_city_data["name"] == "東京", f"tokyo_cityのnameフィールドが一致しません。期待: '東京', 実際: {tokyo_city_data.get('name')}"
            assert "population" in tokyo_city_data, f"'population'フィールドがtokyo_city_dataに存在しません: {tokyo_city_data}"
            expected_population = 13960000
            actual_population = tokyo_city_data.get('population')
            assert actual_population == expected_population, f"tokyo_cityのpopulationフィールドが一致しません。期待: {expected_population}, 実際: {actual_population}"
            
            print("\n=== test_import_all_collections テスト成功 ===\n")
        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)

    def test_litestore_field_conversion(self, db_fixture, export_dir_fixture):
        """LiteStoreフィールド変換機能をテストします。"""
        print("\n=== test_litestore_field_conversion テスト開始 ===\n")
        
        try:
            # フィールド変換テスト用のコレクションを作成
            print("フィールド変換テスト用のコレクションを作成します")
            conversion_col = db_fixture.collection("conversion_test")
    
            # テストデータを作成
            print("テストデータを作成します")
            test_data = {
                "string_field": "test",
                "int_field": 123,
                "float_field": 123.45,
                "bool_field": True,
                "null_field": None,
                "list_field": [1, 2, 3],
                "dict_field": {"key": "value"},
            }
            conversion_col.document("test1").set(test_data)
            print(f"設定したテストデータ: {test_data}")
    
            # エクスポート
            print("\nコレクションをエクスポートします")
            export_result = db_fixture.export_collection("conversion_test", export_dir_fixture)
            print(f"エクスポート結果: {export_result}")
    
            # 新しいデータベースにインポート
            print("\n新しいデータベースにインポートします")
            
            # テスト用の一時的なデータベースファイルを作成
            import os
            import time
            
            # 一時ファイル名を生成
            temp_db_path = os.path.join(
                os.path.dirname(export_dir_fixture),
                f"temp_import_db_{int(time.time() * 1000)}.db"
            )
            print(f"一時データベースファイルを作成します: {temp_db_path}")
            
            # 新しいデータベースを作成
            new_db = LiteStore(db_path=temp_db_path)
            
            # インポートを実行
            import_result = new_db.import_collection("conversion_test", export_dir_fixture)
            print(f"インポート結果: {import_result}")
    
            # インポートされたデータを確認
            print("\nインポートされたデータを確認します")
            new_col = new_db.collection("conversion_test")
            doc = new_col.document("test1").get()
            print(f"取得したドキュメントの型: {type(doc)}")
            print(f"ドキュメントのhasattr(to_dict): {hasattr(doc, 'to_dict')}")
    
            # 結果がDocumentSnapshotオブジェクトか確認
            if hasattr(doc, 'to_dict'):
                doc_data = doc.to_dict()
                print(f"doc_data (from to_dict): {doc_data}")
            else:
                doc_data = doc
                print(f"doc_data (direct): {doc_data}")
    
            # フィールドの型を確認
            print("\nフィールドの型を確認します")
            assert "string_field" in doc_data, f"'string_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert isinstance(doc_data["string_field"], str), f"string_fieldの型が一致しません。期待: str, 実際: {type(doc_data['string_field'])}"
            print(f"string_field: {doc_data['string_field']} (型: {type(doc_data['string_field']).__name__})")
            
            assert "int_field" in doc_data, f"'int_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert isinstance(doc_data["int_field"], int), f"int_fieldの型が一致しません。期待: int, 実際: {type(doc_data['int_field'])}"
            print(f"int_field: {doc_data['int_field']} (型: {type(doc_data['int_field']).__name__})")
            
            assert "float_field" in doc_data, f"'float_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert isinstance(doc_data["float_field"], float), f"float_fieldの型が一致しません。期待: float, 実際: {type(doc_data['float_field'])}"
            print(f"float_field: {doc_data['float_field']} (型: {type(doc_data['float_field']).__name__})")
            
            assert "bool_field" in doc_data, f"'bool_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert isinstance(doc_data["bool_field"], bool), f"bool_fieldの型が一致しません。期待: bool, 実際: {type(doc_data['bool_field'])}"
            print(f"bool_field: {doc_data['bool_field']} (型: {type(doc_data['bool_field']).__name__})")
            
            assert "null_field" in doc_data, f"'null_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert doc_data["null_field"] is None, f"null_fieldの値が一致しません。期待: None, 実際: {doc_data['null_field']}"
            print(f"null_field: {doc_data['null_field']}")
            
            assert "list_field" in doc_data, f"'list_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert isinstance(doc_data["list_field"], list), f"list_fieldの型が一致しません。期待: list, 実際: {type(doc_data['list_field'])}"
            print(f"list_field: {doc_data['list_field']} (型: {type(doc_data['list_field']).__name__})")
            
            assert "dict_field" in doc_data, f"'dict_field'フィールドがdoc_dataに存在しません: {doc_data}"
            assert isinstance(doc_data["dict_field"], dict), f"dict_fieldの型が一致しません。期待: dict, 実際: {type(doc_data['dict_field'])}"
            print(f"dict_field: {doc_data['dict_field']} (型: {type(doc_data['dict_field']).__name__})")
            
            print("\n=== test_litestore_field_conversion テスト成功 ===\n")
        except Exception as e:
            print(f"\n!!! テスト失敗: {e} !!!\n")
            raise


