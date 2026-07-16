import logging
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


LOGGER = logging.getLogger(__name__)


def extract_google_patents(author_name: str) -> List[Dict]:
    """Extract patents from Google Patents for the provided author name."""
    LOGGER.info("Searching for patents for: %s", author_name)
    query_url = f"https://patents.google.com/?q={author_name.replace(' ', '+')}"

    try:
        response = requests.get(query_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        patents: List[Dict] = []
        for result in soup.find_all('tr', class_='result'):
            title_node = result.find('span', class_='title')
            publication_node = result.find('td', class_='publication')

            if not title_node or not publication_node:
                continue

            patent_title = title_node.get_text(strip=True)
            publication_text = publication_node.get_text(strip=True)

            patents.append({
                'title': patent_title,
                'number': publication_text,
                'pub_year': publication_text[:4] if publication_text else 'N/A',
            })

        LOGGER.info("Found %s patents", len(patents))
        return patents

    except requests.RequestException as exc:
        LOGGER.error("Error fetching patents: %s", exc)
        return []
