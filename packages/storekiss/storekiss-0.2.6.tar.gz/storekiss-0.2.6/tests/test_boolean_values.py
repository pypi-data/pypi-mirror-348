#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ブール値の処理に関する単体テスト
"""

import os
import json
import tempfile
import datetime
import pytest

from storekiss import litestore
from storekiss.validation import Schema, BooleanField, StringField
from storekiss.export_import import LiteStoreExporter


@pytest.fixture
def temp_db_path():
    """一時的なデータベースファイルのパスを返すフィクスチャ"""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join("tests/temp_test_data", f"boolean_test_{timestamp}.db")

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


@pytest.fixture
def temp_export_dir():
    """一時的なエクスポートディレクトリを返すフィクスチャ"""
    # tests/temp_test_data ディレクトリに一時ディレクトリを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    export_dir = os.path.join("tests/temp_test_data", f"boolean_export_{timestamp}")
    os.makedirs(export_dir, exist_ok=True)

    yield export_dir

    # テスト後にディレクトリを削除しないようにして、データを保持
    # import shutil
    # if os.path.exists(export_dir):
    #     shutil.rmtree(export_dir)


@pytest.fixture
def db_with_boolean_data(temp_db_path):
    """ブール値を含むデータを持つデータベースを返すフィクスチャ"""
    # スキーマを定義（ブール値フィールドを含む）
    schema = Schema(
        {
            "name": StringField(required=True),
            "is_active": BooleanField(required=True),
            "is_admin": BooleanField(required=False),
        }
    )

    # LiteStoreクライアントを作成 (schema parameter removed as it's no longer supported)
    db = litestore.client(
        db_path=temp_db_path, default_collection="users"
    )

    # ブール値を含むデータを追加
    db.collection("users").document("user1").set(
        {"name": "ユーザー1", "is_active": True, "is_admin": False}
    )

    db.collection("users").document("user2").set({"name": "ユーザー2", "is_active": False})

    return db


class TestBooleanValues:
    """ブール値の処理に関するテスト"""

    def test_boolean_field_storage(self, db_with_boolean_data):
        """ブール値フィールドが正しく保存されることをテスト"""
        # データを取得
        user1 = db_with_boolean_data.collection("users").document("user1").get()
        user2 = db_with_boolean_data.collection("users").document("user2").get()

        user1_data = user1.to_dict()
        user2_data = user2.to_dict()

        # ブール値が正しく保存されていることを確認
        assert user1_data["is_active"] is True
        assert user1_data["is_admin"] is False
        assert user2_data["is_active"] is False
        assert "is_admin" not in user2_data or user2_data["is_admin"] is None  # required=False で default がないため None

    def test_boolean_field_query(self, db_with_boolean_data):
        """ブール値フィールドでのクエリをテスト"""
        # Trueでフィルタリング
        active_users = (
            db_with_boolean_data.collection("users")
            .where("is_active", "==", True)
            .get()
        )
        assert len(active_users) == 1
        active_user_data = active_users[0].to_dict()
        assert active_user_data["name"] == "ユーザー1"

        # Falseでフィルタリング
        inactive_users = (
            db_with_boolean_data.collection("users")
            .where("is_active", "==", False)
            .get()
        )
        assert len(inactive_users) == 1
        inactive_user_data = inactive_users[0].to_dict()
        assert inactive_user_data["name"] == "ユーザー2"

    def test_boolean_field_export(self, db_with_boolean_data, temp_export_dir):
        """ブール値フィールドのエクスポートをテスト"""
        # コレクションをエクスポート
        metadata_file = db_with_boolean_data.export_collection("users", temp_export_dir)

        # メタデータファイルが作成されたことを確認
        assert os.path.exists(metadata_file)

        # JSONLファイルが作成されたことを確認
        jsonl_file = os.path.join(temp_export_dir, "users", "users.jsonl")
        assert os.path.exists(jsonl_file)

        # JSONLファイルの内容を確認
        with open(jsonl_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 2

            # 各ドキュメントを解析
            for line in lines:
                doc = json.loads(line)

                # ブール値フィールドの形式を確認
                if "is_active" in doc["fields"]:
                    # ブール値が integerValue として保存されていることを確認
                    assert "integerValue" in doc["fields"]["is_active"]

                if "is_admin" in doc["fields"]:
                    # user2 の is_admin は null として保存されているか、user1 の is_admin は integerValue として保存されている
                    if "nullValue" in doc["fields"]["is_admin"]:
                        assert doc["fields"]["is_admin"]["nullValue"] is None
                    else:
                        assert "integerValue" in doc["fields"]["is_admin"]

    def test_boolean_field_import(
        self, db_with_boolean_data, temp_export_dir, temp_db_path
    ):
        """ブール値フィールドのインポートをテスト"""
        # コレクションをエクスポート
        db_with_boolean_data.export_collection("users", temp_export_dir)

        # 新しいデータベースを作成 (schema parameter removed as it's no longer supported)
        new_db_path = temp_db_path + ".new"
        new_db = litestore.client(
            db_path=new_db_path, default_collection="users"
        )

        try:
            # エクスポートしたデータをインポート
            imported_count = new_db.import_collection("users", temp_export_dir)
            assert imported_count == 2

            # インポートされたデータを確認
            users = new_db.collection("users").get()
            assert len(users) == 2

            # ブール値が正しくインポートされていることを確認
            for user in users:
                user_data = user.to_dict()
                if user_data["name"] == "ユーザー1":
                    assert user_data["is_active"] is True
                    assert user_data["is_admin"] is False
                elif user_data["name"] == "ユーザー2":
                    assert user_data["is_active"] is False
                    assert "is_admin" not in user_data or user_data["is_admin"] is None

            # ブール値でのクエリが機能することを確認
            active_users = (
                new_db.collection("users").where("is_active", "==", True).get()
            )
            assert len(active_users) == 1
            active_user_data = active_users[0].to_dict()
            assert active_user_data["name"] == "ユーザー1"

        finally:
            # 一時ファイルを削除
            if os.path.exists(new_db_path):
                os.unlink(new_db_path)

    def test_litestore_exporter_boolean_conversion(self, db_with_boolean_data):
        """LiteStoreExporterのブール値変換をテスト"""
        # エクスポーターを作成
        exporter = LiteStoreExporter(db_with_boolean_data)

        # ブール値を含むデータ
        test_data = {
            "bool_true": True,
            "bool_false": False,
            "nested": {"inner_bool": True},
            "array": [True, False, "string", 123],
        }

        # LiteStoreフィールド形式に変換
        litestore_fields = exporter._convert_to_litestore_fields(test_data)

        # 変換結果を確認
        assert "integerValue" in litestore_fields["bool_true"]
        assert litestore_fields["bool_true"]["integerValue"] == "True"

        assert "integerValue" in litestore_fields["bool_false"]
        assert litestore_fields["bool_false"]["integerValue"] == "False"

        # ネストされたブール値
        assert "mapValue" in litestore_fields["nested"]
        nested_fields = litestore_fields["nested"]["mapValue"]["fields"]
        assert "integerValue" in nested_fields["inner_bool"]
        assert nested_fields["inner_bool"]["integerValue"] == "True"

        # 配列内のブール値
        assert "arrayValue" in litestore_fields["array"]
        array_values = litestore_fields["array"]["arrayValue"]["values"]
        assert "integerValue" in array_values[0]
        assert array_values[0]["integerValue"] == "True"
        assert "integerValue" in array_values[1]
        assert array_values[1]["integerValue"] == "False"
