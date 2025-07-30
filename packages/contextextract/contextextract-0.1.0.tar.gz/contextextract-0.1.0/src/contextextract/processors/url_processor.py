import requests
import json
from typing import Dict, Any
from bs4 import BeautifulSoup
from groq import Groq

from ..utils.helpers import handle_api_error


class URLProcessor:
    """
    Process web URLs to extract content as markdown in JSON format.
    """

    def __init__(self, api_key: str):
        """
        Initialize the URL processor with Groq API key.

        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.client = Groq(api_key=api_key)

    def fetch_content(self, url: str) -> str:
        """
        Fetch content from a URL.

        Args:
            url: URL to fetch content from

        Returns:
            Raw HTML content from the URL

        Raises:
            ValueError: If the URL is invalid or unreachable
        """
        try:
            headers = {
                'User-Agent': 'ContextExtract/0.1.0 (Python Package; https://github.com/ssj/contextextract)'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error fetching URL: {e}")

    def convert_to_markdown(self, html_content: str) -> str:
        """
        Convert the HTML content to markdown format.
        Uses BeautifulSoup to extract and preserve important elements.

        Args:
            html_content: HTML content to convert

        Returns:
            Markdown representation of the content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract the page structure and format it as markdown
        markdown_content = ""
        
        # Add page links and headers
        if soup.find('link', rel='canonical'):
            canonical_url = soup.find('link', rel='canonical').get('href')
            markdown_content += f"[Jump to content]({canonical_url}#bodyContent)\n\n"
        
        # Handle semi-protected icons and other page metadata
        for icon in soup.find_all('img', class_='mw-logo-icon'):
            src = icon.get('src', '')
            alt = icon.get('alt', '')
            title = icon.get('title', '')
            markdown_content += f"[![{alt}]({src})]({canonical_url} \"{title}\")\n\n"
        
        # Add "From Wikipedia" header
        markdown_content += "From Wikipedia, the free encyclopedia\n\n"
        
        # Try to extract page description
        if soup.find('p'):
            first_paragraph = soup.find('p').get_text().strip()
            markdown_content += f"{first_paragraph}\n\n"
            
        # Extract redirects and disambiguation
        redirect_section = soup.find('div', {'class': 'redirectMsg'})
        if redirect_section:
            redirect_text = redirect_section.get_text().strip()
            markdown_content += f"\"{redirect_text}\"\n\n"
            
        # Process main content paragraphs and sections
        main_content = soup.find('div', {'id': 'mw-content-text'})
        if main_content:
            for element in main_content.find_all(['p', 'h1', 'h2', 'h3']):
                if element.name.startswith('h'):
                    level = int(element.name[1])
                    heading_text = element.get_text().strip()
                    markdown_content += f"{'#' * level} {heading_text}\n\n"
                else:
                    para_text = element.get_text().strip()
                    if para_text:
                        # Process links inside paragraphs
                        for link in element.find_all('a'):
                            href = link.get('href', '')
                            link_text = link.get_text().strip()
                            # Replace the raw link with markdown format
                            para_text = para_text.replace(link_text, f"[{link_text}]({href})")
                            
                        markdown_content += f"{para_text}\n\n"
        
        return markdown_content

    def process(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a URL to extract content in structured JSON format.

        Args:
            url: URL to process
            params: Parameters for extraction customization

        Returns:
            JSON dictionary with structured content
        """
        try:
            html_content = self.fetch_content(url)
            structured_data = self.convert_to_json(html_content)

            result = {
                "content": structured_data,
                "_metadata": {
                    "source": url,
                    "source_type": "url",
                    "extraction_params": params
                }
            }
            return result

        except Exception as e:
            return {
                "error": str(e),
                "_metadata": {
                    "source": url,
                    "source_type": "url",
                    "extraction_params": params
                }
            }


    def convert_to_json(self, html_content: str) -> Dict[str, Any]:
        """
        Convert the HTML content to a structured JSON format with key-value pairs.

        Args:
            html_content: HTML content to convert

        Returns:
            Dictionary with structured keys like title, summary, and sections
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}

        # Get title
        title_tag = soup.find('title')
        data["title"] = title_tag.get_text().strip() if title_tag else "Untitled"

        # Get summary (first paragraph)
        first_paragraph = soup.find('p')
        if first_paragraph:
            data["summary"] = first_paragraph.get_text().strip()
        
        # Extract canonical URL
        canonical_url = soup.find('link', rel='canonical')
        if canonical_url:
            data["canonical_url"] = canonical_url.get('href')

        # Extract main content sections
        main_content = soup.find('div', {'id': 'mw-content-text'})
        sections = []
        current_section = {"heading": "Introduction", "content": ""}

        if main_content:
            for element in main_content.find_all(['h1', 'h2', 'h3', 'p']):
                if element.name.startswith('h'):
                    # Save current section before switching
                    if current_section["content"].strip():
                        sections.append(current_section)
                    current_section = {
                        "heading": element.get_text().strip(),
                        "content": ""
                    }
                elif element.name == 'p':
                    para_text = element.get_text().strip()
                    if para_text:
                        # Convert links in paragraph
                        for link in element.find_all('a'):
                            href = link.get('href', '')
                            link_text = link.get_text().strip()
                            para_text = para_text.replace(
                                link_text, f"[{link_text}]({href})"
                            )
                        current_section["content"] += para_text + "\n\n"

            # Append last section
            if current_section["content"].strip():
                sections.append(current_section)

        data["sections"] = sections
        return data

