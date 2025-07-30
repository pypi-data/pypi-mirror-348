import json
import re
from typing import Dict, Any, List, Union

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
    error_message = str(error)
    error_type = error.__class__.__name__
    
    # Extract more detailed information from BadRequestError
    if error_type == "BadRequestError" and "json_validate_failed" in error_message:
        try:
            # Try to extract the failed generation from the error message
            match = re.search(r"'failed_generation':\s*'(.*?)'(?=\})", error_message, re.DOTALL)
            if match:
                failed_json = match.group(1).replace('\\n', '\n').replace('\\\\', '\\')
                return {
                    "error": f"{error_type}: JSON validation failed",
                    "error_details": error_message[:100] + "...",
                    "recovery_suggestion": "The LLM generated invalid JSON. Try with a simpler extraction strategy.",
                    "partial_json": failed_json,
                    "success": False
                }
        except:
            pass
    
    return {
        "error": error_message,
        "error_type": error_type,
        "success": False
    }

def chunk_text(text: str, chunk_size: int = 20000, overlap: int = 1000) -> List[str]:
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

def fix_json_response(response_text: str) -> Union[Dict[str, Any], str]:
    """
    Attempt to fix common JSON formatting errors in LLM responses.
    
    Args:
        response_text: The potentially malformed JSON string
        
    Returns:
        Parsed JSON dictionary if successful, or the original string if parsing fails
    """
    try:
        # First try direct parsing
        return json.loads(response_text)
    except json.JSONDecodeError:
        try:
            # Look for JSON object within markdown code blocks
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except:
                    pass
            # 1. Missing quotes around keys
            fixed_text = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', response_text)
            # 2. Trailing commas in arrays and objects
            fixed_text = re.sub(r',\s*([}\]])', r'\1', fixed_text)
            # 3. Missing commas between array elements or object properties
            fixed_text = re.sub(r'(["\w\d])\s*\n\s*("|\w)', r'\1,\2', fixed_text)
            # 4. Ensure all single quotes are replaced with double quotes
            fixed_text = re.sub(r'(?<![\\])\'', '"', fixed_text)
            
            return json.loads(fixed_text)
        except:
            return response_text
