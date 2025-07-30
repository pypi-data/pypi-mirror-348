import requests
import json
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

from ..utils.helpers import handle_api_error

class URLProcessor:
    """
    Process web URLs to extract content as structured JSON, regardless of the website structure.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the URL processor.

        Args:
            api_key: Optional API key for any LLM integration
        """
        self.api_key = api_key

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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error fetching URL: {e}")

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
            structured_data = self.extract_structured_data(html_content, url)
            
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

    def extract_structured_data(self, html_content: str, base_url: str) -> Dict[str, Any]:
        """
        Extract structured data from HTML content, adaptable to any website.

        Args:
            html_content: HTML content to process
            base_url: The original URL for resolving relative URLs

        Returns:
            Dictionary with structured content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        data = {}

        # Get page title
        title_tag = soup.find('title')
        data["title"] = title_tag.get_text().strip() if title_tag else "Untitled"
        
        # Extract description/summary
        description = self._get_meta_description(soup)
        if description:
            data["description"] = description
            
        # Extract canonical URL if available
        canonical = self._get_canonical_url(soup)
        if canonical:
            data["canonical_url"] = canonical
            
        # Extract all links with their text and URLs
        data["links"] = self._extract_links(soup, base_url)
        
        # Extract all matches/events data (specific to sports sites like Cricbuzz)
        data["matches"] = self._extract_matches(soup, base_url)
        
        # Extract news items
        data["news"] = self._extract_news(soup, base_url)
        
        # Extract all text content by main sections
        data["content"] = self._extract_main_content(soup)
        
        return data

    def _get_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description tag content"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and 'content' in meta_desc.attrs:
            return meta_desc['content']
        return None
    
    def _get_canonical_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract canonical URL if present"""
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical and 'href' in canonical.attrs:
            return canonical['href']
        return None
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """Extract all links from the page"""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Handle relative URLs
            full_url = urljoin(base_url, href)
            
            # Clean up the text
            text = a_tag.get_text().strip()
            if text:  # Only include links with text
                link_data = {
                    "text": text,
                    "url": full_url
                }
                
                # Add title attribute if present
                if 'title' in a_tag.attrs:
                    link_data["title"] = a_tag['title']
                    
                links.append(link_data)
                
        return links
    
    def _extract_matches(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """
        Extract match data, primarily for sports websites
        This method looks for common patterns in sports websites
        """
        matches = []
        
        # Look for match containers - this is designed to be flexible across different sites
        # Method 1: Look for containers with match-related classes
        match_containers = soup.find_all(['div', 'li', 'article'], class_=lambda c: c and any(term in str(c).lower() for term in ['match', 'fixture', 'game', 'event', 'contest']))
        
        # If none found, try an alternative approach
        if not match_containers:
            # Look for elements that have teams and scores
            match_containers = soup.find_all(['div', 'li', 'article'], class_=lambda c: c and any(term in str(c).lower() for term in ['team', 'score', 'vs', 'versus']))
        
        # Process each potential match container
        for container in match_containers:
            match_data = {}
            
            # Try to find team names
            teams = []
            team_elements = container.find_all(class_=lambda c: c and any(term in str(c).lower() for term in ['team', 'squad', 'side']))
            
            if team_elements:
                for team in team_elements:
                    teams.append(team.get_text().strip())
            
            # If no team elements found with classes, try to find them by structure
            if not teams:
                # Look for versus or vs text
                vs_pattern = re.compile(r'\bvs\b|\bversus\b', re.IGNORECASE)
                vs_elements = [elem for elem in container.find_all(text=vs_pattern) if vs_pattern.search(elem)]
                
                if vs_elements:
                    for vs_text in vs_elements:
                        parent = vs_text.parent
                        full_text = parent.get_text().strip()
                        # Split by vs/versus to get team names
                        split_text = re.split(vs_pattern, full_text)
                        if len(split_text) >= 2:
                            teams = [part.strip() for part in split_text if part.strip()]
            
            if teams:
                match_data["teams"] = teams
            
            # Try to find match status/result
            status_elements = container.find_all(class_=lambda c: c and any(term in str(c).lower() for term in ['status', 'result', 'state', 'fixture']))
            if status_elements:
                match_data["status"] = status_elements[0].get_text().strip()
            
            # Try to find scores
            score_elements = container.find_all(class_=lambda c: c and any(term in str(c).lower() for term in ['score', 'runs', 'points', 'goals']))
            if score_elements:
                scores = [score.get_text().strip() for score in score_elements]
                match_data["scores"] = scores
            
            # Try to find match time/date
            time_elements = container.find_all(class_=lambda c: c and any(term in str(c).lower() for term in ['time', 'date', 'schedule', 'when']))
            if time_elements:
                match_data["time"] = time_elements[0].get_text().strip()
            
            # Try to find match link
            match_link = container.find('a', href=True)
            if match_link:
                match_data["link"] = urljoin(base_url, match_link['href'])
            
            # If we have any meaningful data, add this match
            if match_data:
                # Get any additional text not captured in specific fields
                match_data["raw_text"] = container.get_text().strip()
                matches.append(match_data)
        
        return matches
    
    def _extract_news(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Extract news items from the page"""
        news_items = []
        
        # Look for news containers
        news_containers = soup.find_all(['div', 'article', 'section'], class_=lambda c: c and any(term in str(c).lower() for term in ['news', 'article', 'story', 'post']))
        
        for container in news_containers:
            news_data = {}
            
            # Try to find title
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong'])
            if title_elem:
                news_data["title"] = title_elem.get_text().strip()
            
            # Try to find link
            link_elem = container.find('a', href=True)
            if link_elem:
                news_data["url"] = urljoin(base_url, link_elem['href'])
                
                # If no title found from headings, use link text
                if 'title' not in news_data and link_elem.get_text().strip():
                    news_data["title"] = link_elem.get_text().strip()
            
            # Try to find time/date
            time_elem = container.find(['time', 'span', 'div'], class_=lambda c: c and any(term in str(c).lower() for term in ['time', 'date', 'published', 'ago']))
            if time_elem:
                news_data["time"] = time_elem.get_text().strip()
            
            # Try to find summary/excerpt
            summary_elem = container.find(['p', 'div'], class_=lambda c: c and any(term in str(c).lower() for term in ['summary', 'excerpt', 'description', 'preview']))
            if summary_elem:
                news_data["summary"] = summary_elem.get_text().strip()
            
            # If we found any useful data, add this news item
            if news_data:
                news_items.append(news_data)
        
        return news_items
    
    def _extract_main_content(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extract the main content organized into sections.
        This is a more generic approach that works across different site structures.
        """
        content_sections = []
        
        # Try to find the main content container
        main_content = None
        main_candidates = [
            soup.find('main'),
            soup.find(id=lambda x: x and 'content' in x.lower()),
            soup.find(id=lambda x: x and 'main' in x.lower()),
            soup.find(class_=lambda x: x and 'content' in x.lower()),
            soup.find(class_=lambda x: x and 'main' in x.lower())
        ]
        
        for candidate in main_candidates:
            if candidate:
                main_content = candidate
                break
        
        # If no main content container found, use the body
        if not main_content:
            main_content = soup.body
        
        if main_content:
            # First, look for clear section divisions with headings
            headings = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
            if headings:
                # Process each heading as a section
                for heading in headings:
                    section = {"heading": heading.get_text().strip(), "content": ""}
                    
                    # Get all content until the next heading
                    current = heading.next_sibling
                    while current and not (current.name and current.name.startswith('h') and int(current.name[1]) <= int(heading.name[1])):
                        if hasattr(current, 'get_text'):
                            text = current.get_text().strip()
                            if text:
                                section["content"] += text + "\n\n"
                        current = current.next_sibling
                    
                    if section["content"]:
                        content_sections.append(section)
            
            # If no clear sections with headings, look for paragraphs
            if not content_sections:
                paragraphs = main_content.find_all('p')
                if paragraphs:
                    all_text = ""
                    for p in paragraphs:
                        text = p.get_text().strip()
                        if text:
                            all_text += text + "\n\n"
                    
                    if all_text:
                        content_sections.append({
                            "heading": "Main Content",
                            "content": all_text
                        })
            
            # If still no content, get all text from the main content
            if not content_sections:
                text = main_content.get_text().strip()
                if text:
                    content_sections.append({
                        "heading": "Content",
                        "content": text
                    })
        
        return content_sections



