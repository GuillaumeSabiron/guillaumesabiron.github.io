from __future__ import annotations

import argparse
import json
import logging
import logging.config
import sys
from pathlib import Path
from typing import Dict, List

from requests import RequestException
from requests.exceptions import ProxyError

from utils.google_patents import extract_google_patents
from utils.google_scholar import extract_google_scholar
from utils.helpers import (
    count_items_by_year,
    load_json_data,
    save_data_to_json,
    save_html,
)
from utils.html_generator import generate_html

LOGGER = logging.getLogger(__name__)


def _setup_logging() -> None:
    """Configure logging using the bundled configuration file if present."""
    config_path = Path(__file__).resolve().parent / 'logging.config'
    if config_path.exists():
        logging.config.fileConfig(config_path, disable_existing_loggers=False)
    elif not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)


def _load_or_fetch_papers(author_name: str, json_filename: str) -> List[Dict]:
    try:
        LOGGER.info("Loading existing data from %s", json_filename)
        data = load_json_data(json_filename)
        return data.get('papers', [])
    except FileNotFoundError:
        LOGGER.info("No cached data found, fetching data for %s", author_name)
        return extract_google_scholar(author_name)


def _filter_out_patents(papers: List[Dict]) -> List[Dict]:
    return [
        paper
        for paper in papers or []
        if not paper.get('bib', {}).get('venue', '').lower().startswith('us patent')
    ]


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Author Publication Fetcher')
    parser.add_argument('--author', type=str, required=True, help='Author Name')
    parser.add_argument('--json_output', type=str, default='author_data.json', help='JSON Output File')
    parser.add_argument('--html_output', type=str, default='papers_list.html', help='HTML Output File')
    args = parser.parse_args(argv)

    _setup_logging()

    author_name = args.author
    json_filename = args.json_output
    html_filename = args.html_output

    try:
        papers = _load_or_fetch_papers(author_name, json_filename)

        if not isinstance(papers, list):
            LOGGER.error("Unexpected JSON structure: expected a list of papers")
            return 1

        papers = _filter_out_patents(papers)
        patents = extract_google_patents(author_name)

        save_data_to_json({'papers': papers, 'patents': patents}, json_filename)

        (
            conference_counts,
            journal_counts,
            patent_counts,
            years,
            total_conference_papers,
            total_journal_papers,
            total_patents,
        ) = count_items_by_year(papers, patents)

        LOGGER.info("Years considered: %s", years)
        LOGGER.info("Conference papers per year: %s", conference_counts)
        LOGGER.info("Journal papers per year: %s", journal_counts)
        LOGGER.info("Patents per year: %s", patent_counts)
        LOGGER.info("Total conference papers: %s", total_conference_papers)
        LOGGER.info("Total journal papers: %s", total_journal_papers)
        LOGGER.info("Total patents: %s", total_patents)

        total_counts: Dict[str, int] = {
            'conference': total_conference_papers,
            'journal': total_journal_papers,
            'patents': total_patents,
        }

        html_content = generate_html(papers, total_counts)
        save_html(html_content, html_filename)

        return 0

    except (FileNotFoundError, json.JSONDecodeError) as exc:
        LOGGER.error("Error loading JSON data from %s: %s", json_filename, exc)
    except (TypeError, ValueError) as exc:
        LOGGER.error("Type or value error occurred: %s", exc)
    except (ProxyError, RequestException) as exc:
        LOGGER.error("Network error while fetching data: %s", exc)
    except ImportError as exc:
        LOGGER.error("Missing dependency: %s", exc)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.exception("Unexpected error occurred", exc_info=exc)

    return 1


if __name__ == "__main__":
    default_author = "Guillaume Sabiron"
    default_json_output = "./data/sabiron_publications.json"
    default_html_output = "./data/sabiron_publications.html"

    if len(sys.argv) == 1:
        sys.argv = [
            sys.argv[0],
            f"--author={default_author}",
            f"--json_output={default_json_output}",
            f"--html_output={default_html_output}",
        ]

    raise SystemExit(main(sys.argv[1:]))
