import os
import json
from typing import Dict, Any, Optional, List
from pypdf import PdfReader
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

            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"

            return clean_text(text)

        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")

    def _split_text_into_chunks(self, text: str, chunk_size: int = 4000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks of specified size with overlap.

        Args:
            text: Text to split
            chunk_size: Maximum size of each chunk in characters
            overlap: Number of characters to overlap between chunks

        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                look_back_start = end - int(chunk_size * 0.2)
                paragraph_break = text.rfind("\n\n", look_back_start, end)
                if paragraph_break != -1:
                    end = paragraph_break + 2
                else:
                    sentence_break = text.rfind(". ", look_back_start, end)
                    if sentence_break != -1:
                        end = sentence_break + 2

            chunks.append(text[start:end])
            start = max(start, end - overlap)
            if start >= len(text):
                break

        return chunks

    def _merge_extracted_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge results from multiple API calls.

        Args:
            results: List of dictionaries containing extracted key-value pairs

        Returns:
            Merged dictionary of key-value pairs
        """
        merged = {}

        for result in results:
            if "error" in result:
                continue

            for key, value in result.items():
                if key in merged:
                    if isinstance(merged[key], str) and isinstance(value, str):
                        merged[key] = f"{merged[key]} {value}"
                    elif isinstance(merged[key], list) and isinstance(value, list):
                        merged[key].extend(value)
                    elif isinstance(merged[key], dict) and isinstance(value, dict):
                        merged[key].update(value)
                else:
                    merged[key] = value

        return merged

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
            model = params.get('model', 'llama3-70b-8192')
            chunk_size = params.get('chunk_size', 4000)
            chunk_overlap = params.get('chunk_overlap', 100)

            chunks = self._split_text_into_chunks(content, chunk_size, chunk_overlap)
            system_message = params.get(
                'system_message',
                "You are an expert information extractor. Extract key information from the provided PDF content "
                "as a structured JSON with key-value pairs. Focus on factual information, "
                "definitions, concepts, and relationships. Return only valid JSON."
            )

            results = []
            chunk_count = len(chunks)

            for i, chunk in enumerate(chunks):
                chunk_system_message = system_message
                if chunk_count > 1:
                    chunk_system_message += f" This is chunk {i+1} of {chunk_count} from the document."

                user_message = f"Extract key-value pairs from the following PDF content and format as JSON:\n\n{chunk}"

                try:
                    chat_completion = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": chunk_system_message},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=0.2,
                        max_tokens=1500,
                        response_format={"type": "json_object"}
                    )

                    response_text = chat_completion.choices[0].message.content
                    try:
                        chunk_result = json.loads(response_text)
                        results.append(chunk_result)
                    except json.JSONDecodeError:
                        results.append({
                            "error": "Failed to parse JSON response",
                            "raw_response": response_text,
                            "chunk_index": i
                        })
                except Exception as e:
                    results.append({
                        "error": f"API error processing chunk {i+1}: {str(e)}",
                        "chunk_index": i
                    })

            if not results:
                return {"error": "No results generated from any chunks"}

            if len(results) == 1:
                return results[0]

            merged_result = self._merge_extracted_results(results)

            return merged_result

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
        try:
            content = self.extract_text_from_pdf(pdf_path)
        except ValueError as e:
            return {
                "error": str(e),
                "error_type": "PDFExtractionError",
                "success": False,
                "_metadata": {
                    "source": pdf_path,
                    "source_type": "pdf",
                    "extraction_params": params
                }
            }

        result = self.extract_key_values(content, params)

        if isinstance(result, dict):
            result["_metadata"] = {
                "source": pdf_path,
                "source_type": "pdf",
                "extraction_params": params
            }

            if "success" not in result and "error" not in result:
                result["success"] = True
            elif "error" in result and "success" not in result:
                result["success"] = False

        return result
