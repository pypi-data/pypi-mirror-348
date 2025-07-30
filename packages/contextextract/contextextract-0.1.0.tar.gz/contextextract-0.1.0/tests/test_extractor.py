
import unittest
import json
from unittest.mock import patch, MagicMock

from contextextract import ContextExtractor
import sys
import os

# Add the src/ directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestContextExtractor(unittest.TestCase):
    """
    Test suite for ContextExtractor class.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.api_key = "gsk_test_key"
        self.extractor = ContextExtractor(api_key=self.api_key)
        
    @patch('contextextract.processors.url_processor.URLProcessor.fetch_content')
    @patch('contextextract.processors.url_processor.URLProcessor.extract_key_values')
    def test_extract_from_url(self, mock_extract, mock_fetch):
        """Test extract_from_url method."""
        # Mock responses
        mock_fetch.return_value = "Mock content"
        mock_extract.return_value = {"key": "value"}
        
        # Call the method
        result = self.extractor.extract_from_url("https://example.com")
        
        # Assertions
        mock_fetch.assert_called_once_with("https://example.com")
        mock_extract.assert_called_once()
        self.assertEqual(result["key"], "value")
        self.assertEqual(result["_metadata"]["source"], "https://example.com")
        
    @patch('contextextract.processors.pdf_processor.PDFProcessor.extract_text_from_pdf')
    @patch('contextextract.processors.pdf_processor.PDFProcessor.extract_key_values')
    def test_extract_from_pdf(self, mock_extract, mock_read_pdf):
        """Test extract_from_pdf method."""
        # Mock responses
        mock_read_pdf.return_value = "Mock PDF content"
        mock_extract.return_value = {"key": "value"}
        
        # Call the method
        result = self.extractor.extract_from_pdf("test.pdf")
        
        # Assertions
        mock_read_pdf.assert_called_once_with("test.pdf")
        mock_extract.assert_called_once()
        self.assertEqual(result["key"], "value")
        self.assertEqual(result["_metadata"]["source"], "test.pdf")
        
    @patch('contextextract.processors.text_processor.TextProcessor.extract_key_values')
    def test_extract_from_text(self, mock_extract):
        """Test extract_from_text method."""
        # Mock responses
        mock_extract.return_value = {"key": "value"}
        
        # Call the method
        result = self.extractor.extract_from_text("Test content")
        
        # Assertions
        mock_extract.assert_called_once()
        self.assertEqual(result["key"], "value")
        self.assertEqual(result["_metadata"]["source_type"], "text")
        
    def test_save_to_json(self):
        """Test save_to_json method."""
        # Test data
        test_data = {"key": "value"}
        test_file = "test_output.json"
        
        # Call the method
        self.extractor.save_to_json(test_data, test_file)
        
        # Assertions
        self.assertTrue(os.path.exists(test_file))
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
