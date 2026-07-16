import json
import logging
from typing import Dict, List

import scholarly


LOGGER = logging.getLogger(__name__)


def extract_google_scholar(author_name: str) -> List[Dict]:
    """Return a list of publications for the given author using the scholarly API."""
    LOGGER.info("Searching for author: %s", author_name)
    try:
        search_query = scholarly.search_author(author_name)
        author = next(search_query)
        LOGGER.info("Author found: %s", author['name'])
    except StopIteration:
        LOGGER.error("No author found with the name %s", author_name)
        return []

    # Fetch author details including publications
    author = scholarly.fill(author)
    publications = author.get('publications', [])

    papers = []
    for pub in publications:
        try:
            pub = scholarly.fill(pub)
            paper = json.loads(json.dumps(pub, default=str))
            papers.append(paper)
        except Exception as e:
            LOGGER.error("Error processing paper: %s", e)
            continue

    return papers
