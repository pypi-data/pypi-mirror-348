import os
import json
import sqlite3
from storekiss.crud import LiteStore

# Create a test database
db_path = "test_rebuild_indexes.db"
if os.path.exists(db_path):
    os.remove(db_path)

# Initialize the store
store = LiteStore(db_path=db_path)

# Create a collection and add some documents
collection = store.collection("test_collection")
collection.add({"name": "Document 1", "value": 100, "active": True})
collection.add({"name": "Document 2", "value": 200, "active": False})
collection.add({"name": "Document 3", "value": 300, "active": True})

# Create another collection with different fields
collection2 = store.collection("another_collection")
collection2.add({"title": "Item A", "price": 10.5, "tags": ["tag1", "tag2"]})
collection2.add({"title": "Item B", "price": 20.75, "tags": ["tag2", "tag3"]})

print("Collections created with test data")

# Manually check if any indexes exist
def check_indexes(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE '%autoindex%'")
    indexes = cursor.fetchall()
    conn.close()
    return [idx[0] for idx in indexes]

print("\nIndexes before rebuild:")
print(check_indexes(db_path))

# Rebuild indexes for all collections
result = store.rebuild_indexes()
print("\nRebuild result:")
print(json.dumps(result, indent=2))

# Check indexes after rebuild
print("\nIndexes after rebuild:")
print(check_indexes(db_path))

# Test rebuilding for a specific collection
result = store.rebuild_indexes(collection_name="test_collection")
print("\nRebuild result for specific collection:")
print(json.dumps(result, indent=2))

print("\nTest completed successfully")
