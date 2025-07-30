# stream() Method in storekiss Library

## Overview

The `stream()` method is designed to efficiently retrieve collection or query results in batches. It provides compatibility with Firestore's namesake method and optimizes memory usage and performance when dealing with large datasets.

## Features

- Retrieves documents in batches and returns them as an iterator
- Processes large amounts of data with minimal memory footprint
- Compatible with both SQLite and PostgreSQL (future extensibility)
- Provides a Firestore-compatible API

## Usage

### Basic Usage

```python
db = litestore.Client("my_database.db")
collection_ref = db.collection("users")

# Use the stream() method to retrieve documents sequentially
for doc in collection_ref.stream():
    print(f"Document ID: {doc.id}, Data: {doc.to_dict()}")
```

### Specifying Batch Size

```python
# Specify batch size for efficient retrieval (default is 20)
for doc in collection_ref.stream(batch_size=10):
    print(f"Document ID: {doc.id}, Data: {doc.to_dict()}")
```

### Combining with Queries

```python
# Combining with where queries
query = collection_ref.where("age", ">=", 30)
for doc in query.stream():
    print(f"Document ID: {doc.id}, Age: {doc.to_dict().get('age')}")

# Combining multiple conditions
query = collection_ref.where("age", ">=", 30).where("city", "==", "Tokyo")
for doc in query.stream(batch_size=5):
    print(f"Document ID: {doc.id}, Data: {doc.to_dict()}")

# Combining with order_by
query = collection_ref.order_by("created_at", direction="DESC").limit(10)
for doc in query.stream():
    print(f"Document ID: {doc.id}, Created At: {doc.to_dict().get('created_at')}")
```

### Updating Documents

```python
# Efficiently update a large number of documents using stream()
for doc in collection_ref.stream(batch_size=50):
    doc_id = doc.id
    doc_ref = collection_ref.document(doc_id)
    doc_ref.update({"processed": True})
```

## Technical Details

### Implementation Overview

The `stream()` method internally uses `limit()` and `offset()` to implement batch processing. Each batch retrieves a specified number of documents and returns them sequentially as an iterator.

```python
def stream(self, batch_size: int = 20):
    # Initialize for batch processing
    offset = 0
    
    while True:
        # Get documents for the current batch
        query = self._collection.limit(batch_size)
        if offset > 0:
            query = query.offset(offset)
            
        # Execute the query
        batch = query.get()
        
        # Exit if no results
        if not batch:
            break
            
        # Return each document sequentially
        for doc in batch:
            yield doc
            
        # Exit if we got fewer documents than the batch size
        # (indicates we've reached the end)
        if len(batch) < batch_size:
            break
            
        # Update offset for the next batch
        offset += batch_size
```

### SQL Query Optimization

Internally, the following SQL queries are generated:

1. First batch:
   ```sql
   SELECT id, data FROM "collection_name" LIMIT ?
   ```

2. Subsequent batches:
   ```sql
   SELECT id, data FROM "collection_name" LIMIT ? OFFSET ?
   ```

3. With conditions:
   ```sql
   SELECT id, data FROM "collection_name" WHERE json_extract(data, '$.field') >= ? LIMIT ? OFFSET ?
   ```

## Performance Considerations

- Too large batch sizes increase memory usage
- Too small batch sizes increase the number of database queries
- Generally, a batch size between 10 and 100 is recommended depending on your processing needs
- Creating appropriate indexes can improve performance when processing large amounts of data

## Future Extensibility

This implementation is designed with future PostgreSQL support in mind. It's structured to provide similar batch processing capabilities for both SQLite and PostgreSQL databases.
