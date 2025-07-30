"""
Test for iteration check example.

This test verifies the functionality of the iteration_check_example.py script.
"""

import unittest
from unittest.mock import patch, MagicMock
import datetime
import sys
import os

# Add the parent directory to sys.path to import the example module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples import iteration_check_example


class TestIterationCheck(unittest.TestCase):
    """Test cases for iteration check example."""

    def test_generate_test_data(self):
        """Test that test data is generated correctly."""
        # Test with default count
        data = iteration_check_example.generate_test_data()
        self.assertEqual(len(data), 10)
        
        # Test with custom count
        data = iteration_check_example.generate_test_data(5)
        self.assertEqual(len(data), 5)
        
        # Check structure of generated data
        for i, item in enumerate(data):
            self.assertEqual(item['name'], f'User {i}')
            self.assertEqual(item['age'], 20 + i)
            self.assertEqual(item['email'], f'user{i}@example.com')
            self.assertIsInstance(item['created_at'], datetime.datetime)
            self.assertEqual(item['active'], i % 2 == 0)
            self.assertEqual(item['score'], float(i * 10))
            self.assertNotIn('check', item)

    @patch('examples.iteration_check_example.uuid.uuid4')
    def test_create_test_documents(self, mock_uuid):
        """Test creating test documents."""
        # Mock UUID generation
        mock_uuid.side_effect = [f'uuid-{i}' for i in range(3)]
        
        # Create mock collection reference
        mock_collection = MagicMock()
        mock_doc_ref = MagicMock()
        mock_collection.document.return_value = mock_doc_ref
        
        # Test data
        test_data = [
            {'name': 'User 1'},
            {'name': 'User 2'},
            {'name': 'User 3'}
        ]
        
        # Call function
        doc_ids = iteration_check_example.create_test_documents(mock_collection, test_data)
        
        # Verify results
        self.assertEqual(len(doc_ids), 3)
        self.assertEqual(doc_ids, ['uuid-0', 'uuid-1', 'uuid-2'])
        
        # Verify mock calls
        self.assertEqual(mock_collection.document.call_count, 3)
        self.assertEqual(mock_doc_ref.set.call_count, 3)
        
        # Verify document creation with correct data
        for i, data in enumerate(test_data):
            mock_collection.document.assert_any_call(f'uuid-{i}')
            mock_doc_ref.set.assert_any_call(data)

    def test_update_documents_with_check(self):
        """Test updating documents with check=True."""
        # Create mock collection reference
        mock_collection = MagicMock()
        mock_doc_ref = MagicMock()
        
        # Mock document data
        mock_doc1 = {'id': 'doc1', 'name': 'User 1'}
        mock_doc2 = {'id': 'doc2', 'name': 'User 2'}
        mock_doc3 = {'id': 'doc3', 'name': 'User 3'}
        
        mock_docs = [mock_doc1, mock_doc2, mock_doc3]
        
        # Setup mock returns
        mock_collection.get.return_value = mock_docs
        mock_collection.document.return_value = mock_doc_ref
        
        # Call function
        updated_count = iteration_check_example.update_documents_with_check(mock_collection)
        
        # Verify results
        self.assertEqual(updated_count, 3)
        
        # Verify mock calls
        self.assertEqual(mock_collection.document.call_count, 3)
        self.assertEqual(mock_doc_ref.update.call_count, 3)
        
        # Verify document updates with check=True
        for doc in mock_docs:
            mock_collection.document.assert_any_call(doc['id'])
            mock_doc_ref.update.assert_any_call({'check': True})

    def test_verify_updates(self):
        """Test verification of updates."""
        # Create mock collection reference
        mock_collection = MagicMock()
        
        # Test case 1: All documents have check=True
        mock_doc1 = {'id': 'doc1', 'check': True}
        mock_doc2 = {'id': 'doc2', 'check': True}
        mock_doc3 = {'id': 'doc3', 'check': True}
        
        mock_collection.get.return_value = [mock_doc1, mock_doc2, mock_doc3]
        
        self.assertTrue(iteration_check_example.verify_updates(mock_collection))
        
        # Test case 2: Some documents don't have check=True
        mock_doc2 = {'id': 'doc2', 'check': False}
        mock_collection.get.return_value = [mock_doc1, mock_doc2, mock_doc3]
        
        self.assertFalse(iteration_check_example.verify_updates(mock_collection))
        
        # Test case 3: Some documents don't have check field
        mock_doc2 = {'id': 'doc2'}
        mock_collection.get.return_value = [mock_doc1, mock_doc2, mock_doc3]
        
        self.assertFalse(iteration_check_example.verify_updates(mock_collection))

    @patch('examples.iteration_check_example.litestore.Client')
    @patch('examples.iteration_check_example.generate_test_data')
    @patch('examples.iteration_check_example.create_test_documents')
    @patch('examples.iteration_check_example.update_documents_with_check')
    @patch('examples.iteration_check_example.verify_updates')
    def test_main(self, mock_verify, mock_update, mock_create, mock_generate, mock_client):
        """Test the main function."""
        # Setup mocks
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_client.return_value = mock_db
        mock_db.collection.return_value = mock_collection
        
        mock_generate.return_value = [{'name': f'User {i}'} for i in range(10)]
        mock_create.return_value = [f'doc{i}' for i in range(10)]
        mock_update.return_value = 10
        mock_verify.return_value = True
        
        # Call main function
        iteration_check_example.main()
        
        # Verify calls
        mock_client.assert_called_once()
        mock_db.collection.assert_called_once_with('iteration_check_test')
        mock_generate.assert_called_once_with(10)
        mock_create.assert_called_once()
        mock_update.assert_called_once_with(mock_collection)
        mock_verify.assert_called_once_with(mock_collection)


if __name__ == '__main__':
    unittest.main()
