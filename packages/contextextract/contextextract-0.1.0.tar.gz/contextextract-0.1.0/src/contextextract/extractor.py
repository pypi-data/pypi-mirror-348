import os
from typing import Dict, List, Any, Optional, Union
import json

from .processors.url_processor import URLProcessor
from .processors.pdf_processor import PDFProcessor
from .processors.text_processor import TextProcessor
from .utils.helpers import validate_api_key


class ContextExtractor:
    """
    Main class for extracting key-value pairs from various sources using Groq API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ContextExtractor with Groq API key.
        
        Args:
            api_key: Groq API key. If None, looks for GROQ_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        validate_api_key(self.api_key)
        
        # Initialize processors
        self.url_processor = URLProcessor(self.api_key)
        self.pdf_processor = PDFProcessor(self.api_key)
        self.text_processor = TextProcessor(self.api_key)
    
    def extract_from_url(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract key-value pairs from a URL.
        
        Args:
            url: The URL to extract data from
            params: Optional parameters for extraction customization
            
        Returns:
            Dictionary containing key-value pairs extracted from the URL
        """
        return self.url_processor.process(url, params or {})
    
    def extract_from_pdf(self, pdf_path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract key-value pairs from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            params: Optional parameters for extraction customization
            
        Returns:
            Dictionary containing key-value pairs extracted from the PDF
        """
        return self.pdf_processor.process(pdf_path, params or {})
    
    def extract_from_text(self, text: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract key-value pairs from text.
        
        Args:
            text: Input text to extract data from
            params: Optional parameters for extraction customization
            
        Returns:
            Dictionary containing key-value pairs extracted from the text
        """
        return self.text_processor.process(text, params or {})
    
    @staticmethod
    def save_to_json(data: Dict[str, Any], output_path: str, pretty: bool = True) -> None:
        """
        Save extracted data to a JSON file.
        
        Args:
            data: Extracted key-value pairs
            output_path: Path to save the JSON file
            pretty: Whether to format the JSON with indentation
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
