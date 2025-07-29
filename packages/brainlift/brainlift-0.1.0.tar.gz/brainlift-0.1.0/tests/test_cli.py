#!/usr/bin/env python3
"""
Tests for the BrainLift CLI
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to import blm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import blm

class TestBrainLiftCLI(unittest.TestCase):
    """Test cases for the BrainLift CLI"""
    
    @patch('blm.call_serverless_api')
    def test_list_command(self, mock_call_api):
        """Test the list command"""
        # Mock the API response
        mock_call_api.return_value = {
            'success': True,
            'products': ['test_product']
        }
        
        # Call the list_content function
        with patch('sys.argv', ['blm', 'list']):
            result = blm.main()
        
        # Check that the API was called correctly
        mock_call_api.assert_called_once()
        self.assertEqual(mock_call_api.call_args[0][0], 'list')
        self.assertEqual(result, 0)
    
    @patch('blm.call_serverless_api')
    def test_search_command(self, mock_call_api):
        """Test the search command"""
        # Mock the API response
        mock_call_api.return_value = {
            'success': True,
            'results': [
                {'title': 'Test Result', 'score': 0.95, 'path': 'test/path', 'content': 'Test content'}
            ]
        }
        
        # Call the search_content function
        with patch('sys.argv', ['blm', 'search', 'test query']):
            result = blm.main()
        
        # Check that the API was called correctly
        mock_call_api.assert_called_once()
        self.assertEqual(mock_call_api.call_args[0][0], 'search')
        self.assertEqual(mock_call_api.call_args[0][1]['query'], 'test query')
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
