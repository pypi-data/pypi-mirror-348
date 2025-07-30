import os
import json
from typing import Dict, Any, Optional
from PyPDF2 import PdfReader
from groq import Groq

from ..utils.helpers import clean_text, handle_api_error


class PDFProcessor:
    """
    Process PDF files to extract key-value pairs using Groq API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the PDF processor with Groq API key.
        
        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content from the PDF
            
        Raises:
            ValueError: If the PDF file is invalid or cannot be read
        """
        try:
            if not os.path.exists(pdf_path):
                raise ValueError(f"PDF file not found: {pdf_path}")
                
            pdf_reader = PdfReader(pdf_path)
            text = ""
            
            # Extract text from each page
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
                
            return clean_text(text)
            
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")
    
    def extract_key_values(self, content: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key-value pairs from content using Groq API.
        
        Args:
            content: Text content to extract data from
            params: Parameters for extraction customization
            
        Returns:
            Dictionary of key-value pairs
        """
        try:
            # Determine what model to use, defaulting to LLaMA3-70b-8192
            model = params.get('model', 'llama3-70b-8192')
            
            # Prepare system message
            system_message = params.get('system_message', 
                "You are an expert information extractor. Extract key information from the provided PDF content "
                "as a structured JSON with key-value pairs. Focus on factual information, "
                "definitions, concepts, and relationships. Return only valid JSON."
            )
            
            # Prepare user message with content
            user_message = f"Extract key-value pairs from the following PDF content and format as JSON:\n\n{content[:25000]}"
            
            # Make the API call
            chat_completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # Extract and parse JSON response
            response_text = chat_completion.choices[0].message.content
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw text in a structured format
                return {"error": "Failed to parse JSON response", "raw_response": response_text}
                
        except Exception as e:
            return handle_api_error(e)
    
    def process(self, pdf_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a PDF file to extract key-value pairs.
        
        Args:
            pdf_path: Path to the PDF file
            params: Parameters for extraction customization
            
        Returns:
            Dictionary of key-value pairs extracted from the PDF
        """
        content = self.extract_text_from_pdf(pdf_path)
        result = self.extract_key_values(content, params)
        
        # Add metadata to the result
        result["_metadata"] = {
            "source": pdf_path,
            "source_type": "pdf",
            "extraction_params": params
        }
        
        return result
