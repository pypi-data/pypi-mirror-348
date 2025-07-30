"""
Tests for the CRUD operations.
"""
import os
import pytest
from storekiss.crud import LiteStore
from storekiss.exceptions import NotFoundError, ValidationError
from storekiss.validation import (
    Schema,
    StringField,
    NumberField,
    BooleanField,
    MapField,
)
import datetime


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    # tests/temp_test_data ディレクトリに一時ファイルを作成
    os.makedirs("tests/temp_test_data", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    db_path = os.path.join("tests/temp_test_data", f"crud_test_{timestamp}.db")

    yield db_path

    # テスト後にファイルを削除しないようにして、データを保持
    # if os.path.exists(db_path):
    #     os.unlink(db_path)


@pytest.fixture
def simple_store(temp_db_path):
    """Create a simple store without schema validation."""
    return LiteStore(db_path=temp_db_path)


@pytest.fixture
def user_schema():
    """Create a schema for user data."""
    return Schema(
        {
            "name": StringField(required=True, min_length=2),
            "age": NumberField(required=True, min_value=0, integer_only=True),
            "email": StringField(required=True),
            "active": BooleanField(required=False),
            "address": MapField(
                {
                    "street": StringField(required=True),
                    "city": StringField(required=True),
                    "zip": StringField(required=True),
                },
                required=False,
            ),
        }
    )


@pytest.fixture
def user_store(temp_db_path):
    """Create a store for user data."""
    return LiteStore(
        db_path=temp_db_path, default_collection="users"
    )


class TestLiteStore:
    """Tests for the LiteStore class."""

    def test_create_and_read(self, simple_store):
        """Test creating and reading an item."""
        data = {"name": "Test Item", "value": 42}
        item = simple_store.create(data)

        assert "id" in item
        assert item["name"] == "Test Item"
        assert item["value"] == 42

        read_item = simple_store.read(item["id"])
        assert read_item == item

    def test_create_with_custom_id(self, simple_store):
        """Test creating an item with a custom ID."""
        data = {"name": "Custom ID Item"}
        item = simple_store.create(data, id="custom-id")

        assert item["id"] == "custom-id"
        assert item["name"] == "Custom ID Item"

        read_item = simple_store.read("custom-id")
        assert read_item == item

    def test_update(self, simple_store):
        """Test updating an item."""
        data = {"name": "Original Name", "value": 42}
        item = simple_store.create(data)
        item_id = item["id"]

        updated = simple_store.update(item_id, {"name": "Updated Name"})
        assert updated["id"] == item_id
        assert updated["name"] == "Updated Name"
        assert updated["value"] == 42  # Should be preserved with merge=True

        read_item = simple_store.read(item_id)
        assert read_item == updated

    def test_update_replace(self, simple_store):
        """Test updating an item with replace (merge=False)."""
        data = {"name": "Original Name", "value": 42}
        item = simple_store.create(data)
        item_id = item["id"]

        updated = simple_store.update(item_id, {"name": "Updated Name"}, merge=False)
        assert updated["id"] == item_id
        assert updated["name"] == "Updated Name"
        assert "value" not in updated  # Should be removed with merge=False

        read_item = simple_store.read(item_id)
        assert read_item == updated

    def test_delete(self, simple_store):
        """Test deleting an item."""
        data = {"name": "Item to Delete"}
        item = simple_store.create(data)
        item_id = item["id"]

        simple_store.delete(item_id)

        with pytest.raises(NotFoundError):
            simple_store.read(item_id)

    def test_list(self, simple_store):
        """Test listing items."""
        simple_store.create({"name": "Item 1"})
        simple_store.create({"name": "Item 2"})
        simple_store.create({"name": "Item 3"})

        items = simple_store.list()
        assert len(items) == 3

        limited = simple_store.list(limit=2)
        assert len(limited) == 2

        offset = simple_store.list(offset=1)
        assert len(offset) == 2

    def test_query(self, simple_store):
        """Test querying items."""
        simple_store.create({"name": "Alice", "age": 30, "city": "New York"})
        simple_store.create({"name": "Bob", "age": 25, "city": "Boston"})
        simple_store.create({"name": "Charlie", "age": 35, "city": "New York"})

        ny_items = simple_store.query({"city": "New York"})
        assert len(ny_items) == 2
        assert all(item.to_dict()["city"] == "New York" for item in ny_items)

        young_items = simple_store.query({"age": 25})
        assert len(young_items) == 1
        assert young_items[0].to_dict()["name"] == "Bob"

    def test_count(self, simple_store):
        """Test counting items."""
        simple_store.create({"name": "Item 1", "category": "A"})
        simple_store.create({"name": "Item 2", "category": "B"})
        simple_store.create({"name": "Item 3", "category": "A"})

        assert simple_store.count() == 3

        assert simple_store.count({"category": "A"}) == 2
        assert simple_store.count({"category": "B"}) == 1
        assert simple_store.count({"category": "C"}) == 0

    # スキーマ検証機能を削除したため、このテストケースは不要
    # def test_schema_validation(self, user_store):
    #     """Test schema validation."""
    #     pass
