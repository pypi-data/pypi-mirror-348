import re
import json
from typing import Dict, Any

def clean_text(text: str) -> str:
    """
    Clean and normalize text for better processing.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
    """
    # Replace multiple newlines with a single one
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Replace special characters with proper equivalents
    text = text.replace('\\n', '\n')
    text = text.replace('\\"', '"')
    
    return text.strip()

def validate_api_key(api_key: str) -> None:
    """
    Validate that an API key is provided.
    
    Args:
        api_key: Groq API key to validate
        
    Raises:
        ValueError: If API key is missing
    """
    if not api_key:
        raise ValueError(
            "Groq API key is required. Either pass it directly to the constructor "
            "or set the GROQ_API_KEY environment variable."
        )
    
    # Basic validation - ensure it starts with "gsk_"
    if not api_key.startswith("gsk_"):
        raise ValueError(
            "Invalid Groq API key format. API keys should start with 'gsk_'."
        )

def handle_api_error(error: Exception) -> Dict[str, Any]:
    """
    Handle API errors in a standardized way.
    
    Args:
        error: The exception that occurred
        
    Returns:
        Dictionary with error information
    """
    return {
        "error": str(error),
        "error_type": error.__class__.__name__,
        "success": False
    }

def chunk_text(text: str, chunk_size: int = 20000, overlap: int = 1000) -> list:
    """
    Split text into chunks for processing with overlap.
    
    Args:
        text: Text to split into chunks
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = min(start + chunk_size, text_len)
        
        # If we're not at the end and the chunk doesn't end with whitespace,
        # try to find a good breaking point
        if end < text_len:
            # Look for a period, exclamation mark, or question mark followed by whitespace
            match = re.search(r'[.!?]\s', text[end-100:end])
            if match:
                end = end - 100 + match.end()
            else:
                # If no sentence boundary found, try to break at a space
                space_pos = text.rfind(' ', end - 100, end)
                if space_pos > 0:
                    end = space_pos + 1
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks
