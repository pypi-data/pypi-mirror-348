import json
import re
from typing import Dict, Any, Optional
from groq import Groq

from ..utils.helpers import clean_text, handle_api_error

class TextProcessor:
    """
    Process text input to extract key-value pairs using Groq API.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the text processor with Groq API key.
        
        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
    
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
            
            # Prepare system message with more robust instructions for JSON generation
            system_message = params.get('system_message',
                "You are an expert information extractor. Extract key information from the provided text "
                "as a structured JSON with key-value pairs. Focus on factual information, "
                "definitions, concepts, and relationships. Ensure your response is valid JSON format with "
                "proper quoting of keys and values. Keep the JSON structure simple and flat when possible. "
                "Make sure all keys and string values are enclosed in double quotes and arrays are properly formatted."
            )
            
            # Prepare user message with content
            user_message = f"Extract key-value pairs from the following text and format as valid, parseable JSON:\n\n{content[:25000]}"
            
            # Make the API call with lower temperature for more consistent outputs
            chat_completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # Extract and parse JSON response
            response_text = chat_completion.choices[0].message.content
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                try:
                    fixed_text = re.sub(r'([{,])\s*(\w+):', r'\1"\2":', response_text)
                    fixed_text = re.sub(r'(?<!\\)"(?=(.*?".*?[,}]))', r'\"', fixed_text)
                    return json.loads(fixed_text)
                except (json.JSONDecodeError, re.error):
                    return {
                        "error": "Failed to parse JSON response",
                        "raw_response": response_text,
                        "success": False
                    }
                
        except Exception as e:
            return handle_api_error(e)
    
    def process(self, text: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process text to extract key-value pairs.
        
        Args:
            text: Text to process
            params: Parameters for extraction customization
            
        Returns:
            Dictionary of key-value pairs extracted from the text
        """
        # Clean and prepare the text
        cleaned_text = clean_text(text)
        
        # Process text in chunks if it's very large
        if len(cleaned_text) > 25000 and 'chunk_size' not in params:
            from ..utils.helpers import chunk_text
            chunks = chunk_text(cleaned_text)
            results = []
            
            # Process each chunk
            for i, chunk in enumerate(chunks):
                chunk_result = self.extract_key_values(chunk, params)
                # Add chunk metadata
                if not isinstance(chunk_result, dict) or "error" in chunk_result:
                    # If error in processing, store and continue
                    chunk_result = {"chunk_index": i, "chunk_content": chunk[:100] + "...", "error": str(chunk_result)}
                else:
                    chunk_result["_chunk_metadata"] = {"index": i, "length": len(chunk)}
                results.append(chunk_result)
            
            # Combine results
            combined_result = {}
            
            # If any successful chunks, combine their data
            successful_chunks = [r for r in results if isinstance(r, dict) and "error" not in r]
            for chunk_result in successful_chunks:
                for key, value in chunk_result.items():
                    if key != "_chunk_metadata":
                        if key not in combined_result:
                            combined_result[key] = value
                        elif isinstance(value, list) and isinstance(combined_result[key], list):
                            # Combine lists
                            combined_result[key].extend(value)
                        elif isinstance(value, dict) and isinstance(combined_result[key], dict):
                            # Combine dictionaries
                            combined_result[key].update(value)
            
            # If no successful processing, return the first error
            if not combined_result and results:
                combined_result = results[0]
            
            # Add chunking metadata
            combined_result["_chunking_info"] = {
                "total_chunks": len(chunks),
                "successful_chunks": len(successful_chunks),
                "failed_chunks": len(chunks) - len(successful_chunks)
            }
            
            result = combined_result
        else:
            # Process as a single chunk
            result = self.extract_key_values(cleaned_text, params)
        
        # Add metadata to the result
        if isinstance(result, dict):
            result["_metadata"] = {
                "source_type": "text",
                "text_length": len(text),
                "extraction_params": params
            }
        
        return result
