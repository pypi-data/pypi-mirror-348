"""
Iteration check example.

This example demonstrates how to:
1. Generate 10 test documents
2. Query all documents
3. Update each document by setting check=True field
"""

import datetime
from typing import Dict, Any, List
import uuid

from storekiss import litestore
import logkiss as logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def generate_test_data(count: int = 10) -> List[Dict[str, Any]]:
    """Generate test data documents.

    Args:
        count: Number of documents to generate

    Returns:
        List of document data dictionaries
    """
    test_data = []
    for i in range(count):
        doc_data = {
            'name': f'User {i}',
            'age': 20 + i,
            'email': f'user{i}@example.com',
            'created_at': datetime.datetime.now(),
            'active': i % 2 == 0,  # Even numbers are active
            'score': float(i * 10),
            # check field is intentionally not set initially
        }
        test_data.append(doc_data)
    return test_data


def create_test_documents(collection_ref, test_data: List[Dict[str, Any]]) -> List[str]:
    """Create test documents in the specified collection.

    Args:
        collection_ref: Collection reference
        test_data: List of document data to create

    Returns:
        List of created document IDs
    """
    doc_ids = []
    for data in test_data:
        # Generate a unique ID for each document
        doc_id = str(uuid.uuid4())
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(data)
        doc_ids.append(doc_id)
        logger.debug("Created document with ID: %s", doc_id)
    
    return doc_ids


def update_documents_with_check(collection_ref) -> int:
    """Query all documents and update each with check=True.

    Args:
        collection_ref: Collection reference

    Returns:
        Number of documents updated
    """
    # Get all documents from the collection
    docs = collection_ref.get()
    logger.debug("Found %d documents to update", len(docs))
    
    # Update each document with check=True
    update_count = 0
    for doc in docs:
        # DocumentSnapshotオブジェクトからドキュメントIDを取得
        doc_id = doc['id']
        doc_ref = collection_ref.document(doc_id)
        doc_ref.update({'check': True})
        update_count += 1
        logger.debug("Updated document %s with check=True", doc_id)
    
    return update_count


def verify_updates(collection_ref) -> bool:
    """Verify that all documents have check=True.

    Args:
        collection_ref: Collection reference

    Returns:
        True if all documents have check=True, False otherwise
    """
    docs = collection_ref.get()
    all_checked = True
    
    for doc in docs:
        # ドキュメントデータを取得
        doc_id = doc['id']
        
        if not doc.get('check'):
            all_checked = False
            logger.error("Document %s does not have check=True", doc_id)
    
    return all_checked


def main():
    # Create a LiteStore client
    db = litestore.Client()
    
    # Use a specific collection for this example
    collection_name = 'iteration_check_test'
    collection_ref = db.collection(collection_name)
    
    # Generate test data
    test_data = generate_test_data(10)
    logger.info("Generated %d test documents", len(test_data))
    
    # Create test documents
    doc_ids = create_test_documents(collection_ref, test_data)
    logger.info("Created %d documents in collection '%s'", len(doc_ids), collection_name)
    
    # Update documents with check=True
    updated_count = update_documents_with_check(collection_ref)
    logger.info("Updated %d documents with check=True", updated_count)
    
    # Verify all documents have check=True
    if verify_updates(collection_ref):
        logger.info("✅ All documents have been successfully updated with check=True")
    else:
        logger.error("❌ Some documents were not updated correctly")


if __name__ == "__main__":
    main()
