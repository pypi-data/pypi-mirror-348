"""
配列（リスト）とマップ（辞書）の拡張機能のテスト
"""

import pytest
import datetime
import os
import tempfile
import shutil
from storekiss.litestore import client
from storekiss.validation import (
    ListField, MapField, StringField, NumberField, 
    BooleanField, DateTimeField, Schema, ValidationError
)


@pytest.fixture
def array_db():
    """配列テスト用のデータベース"""
    db_path = "test_array_db.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    db = client(db_path=db_path, default_collection="arrays")
    
    collection = db.collection("arrays")
    
    collection.add({
        "id": "array1",
        "tags": ["python", "database", "sqlite"],
        "scores": [85, 92, 78, 95],
        "mixed": ["text", 123, True, None],
        "matrix": [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0]
        ]
    })
    
    collection.add({
        "id": "array2",
        "tags": ["javascript", "web", "database"],
        "scores": [75, 88, 90],
        "mixed": ["other", 456, False],
        "matrix": [
            [9.0, 8.0],
            [7.0, 6.0],
            [5.0, 4.0]
        ]
    })
    
    return db


@pytest.fixture
def map_db():
    """マップテスト用のデータベース"""
    db_path = "test_map_db.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    db = client(db_path=db_path, default_collection="users")
    
    collection = db.collection("users")
    
    collection.add({
        "name": "山田太郎",
        "age": 35,
        "address": {
            "street": "桜木町1-2-3",
            "city": "東京都",
            "zip": "123-4567"
        },
        "contact": {
            "email": "yamada@example.com",
            "phone": "03-1234-5678"
        }
    }, id="user1")
    
    collection.add({
        "name": "佐藤花子",
        "age": 28,
        "address": {
            "street": "梅田4-5-6",
            "city": "大阪府",
            "zip": "567-8901"
        },
        "contact": {
            "email": "sato@example.com"
        }
    }, id="user2")
    
    return db


@pytest.fixture(scope="module", autouse=True)
def cleanup_test_files():
    """テスト終了後にテストファイルを削除するフィクスチャ"""
    yield
    for file_path in ["test_array_db.sqlite", "test_map_db.sqlite"]:
        if os.path.exists(file_path):
            os.remove(file_path)


class TestArrayExtensions:
    """配列（リスト）の拡張機能のテスト"""
    
    def test_array_type_validation(self):
        """配列の型チェック機能のテスト"""
        string_list = ListField(element_type=str)
        
        assert string_list.validate(["a", "b", "c"]) == ["a", "b", "c"]
        
        with pytest.raises(ValidationError):
            string_list.validate(["a", 123, "c"])
        
        number_list = ListField(element_type=int)
        
        assert number_list.validate([1, 2, 3]) == [1, 2, 3]
        
        with pytest.raises(ValidationError):
            number_list.validate([1, "two", 3])
    
    def test_multidimensional_arrays(self):
        """多次元配列のテスト"""
        matrix = ListField(item_validator=ListField(element_type=float))
        
        valid_matrix = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0]
        ]
        assert matrix.validate(valid_matrix) == valid_matrix
        
        invalid_matrix = [
            [1.0, 2.0, 3.0],
            [4.0, "5.0", 6.0]
        ]
        with pytest.raises(ValidationError):
            matrix.validate(invalid_matrix)
    
    def test_array_contains_query(self, array_db):
        """配列のcontainsクエリのテスト"""
        collection = array_db.collection("arrays")
        
        python_docs = collection.where("tags", "contains", "python").get()
        assert len(python_docs) == 1
        assert python_docs[0].to_dict()["id"] == "array1"
        
        database_docs = collection.where("tags", "contains", "database").get()
        assert len(database_docs) == 2
        
        high_score_docs = collection.where("scores", "contains", 95).get()
        assert len(high_score_docs) == 1
        assert high_score_docs[0].to_dict()["id"] == "array1"
        
        no_docs = collection.where("tags", "contains", "java").get()
        assert len(no_docs) == 0


class TestMapExtensions:
    """マップ（辞書）の拡張機能のテスト"""
    
    def test_nested_field_validation(self):
        """ネストされたフィールドのバリデーションのテスト"""
        schema = Schema({
            "name": StringField(),
            "address.street": StringField(),
            "address.city": StringField(),
            "address.zip": StringField(required=False),
        })
        
        valid_data = {
            "name": "山田太郎",
            "address": {
                "street": "桜木町1-2-3",
                "city": "東京都",
                "zip": "123-4567"
            }
        }
        validated = schema.validate(valid_data)
        assert validated["name"] == "山田太郎"
        assert validated["address"]["street"] == "桜木町1-2-3"
        
        invalid_data = {
            "name": "山田太郎",
            "address": {
                "street": "桜木町1-2-3",
            }
        }
        with pytest.raises(ValidationError):
            schema.validate(invalid_data)
    
    def test_nested_field_query(self, map_db):
        """ネストされたフィールドのクエリのテスト"""
        collection = map_db.collection("users")
        
        tokyo_users = collection.where("address.city", "==", "東京都").get()
        assert len(tokyo_users) == 1
        assert tokyo_users[0].to_dict()["name"] == "山田太郎"
        
        osaka_users = collection.where("address.city", "==", "大阪府").get()
        assert len(osaka_users) == 1
        assert osaka_users[0].to_dict()["name"] == "佐藤花子"
        
        no_users = collection.where("address.city", "==", "京都府").get()
        assert len(no_users) == 0
    
    def test_partial_update(self, map_db):
        """ネストされたフィールドの部分更新のテスト"""
        collection = map_db.collection("users")
        
        user_doc = collection.document("user1")
        
        user_doc.update({
            "address.street": "新宿区1-2-3",
            "contact.phone": "090-1234-5678"
        })
        
        updated_user = user_doc.get().to_dict()
        
        assert updated_user["address"]["street"] == "新宿区1-2-3"
        assert updated_user["contact"]["phone"] == "090-1234-5678"
        
        assert updated_user["address"]["city"] == "東京都"
        assert updated_user["address"]["zip"] == "123-4567"
        assert updated_user["contact"]["email"] == "yamada@example.com"
