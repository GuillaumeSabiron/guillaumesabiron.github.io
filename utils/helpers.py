import json
import logging
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

LOGGER = logging.getLogger(__name__)


def load_json_data(filename: str) -> Dict:
    """Load JSON data from a file and return the resulting dictionary."""
    try:
        with open(filename, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        LOGGER.error("Unable to load JSON from %s: %s", filename, exc)
        raise


def _ensure_parent_dir(filename: str) -> None:
    Path(filename).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def save_data_to_json(data: Dict, filename: str) -> None:
    """Persist a dictionary to disk as JSON, creating parent directories if needed."""
    try:
        _ensure_parent_dir(filename)
        with open(filename, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        LOGGER.info("Data saved to %s", filename)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.error("Failed to save JSON data to %s: %s", filename, exc)
        raise


def save_html(html_content: str, filename: str) -> None:
    """Persist HTML content to disk, ensuring the destination path exists."""
    try:
        _ensure_parent_dir(filename)
        with open(filename, 'w', encoding='utf-8') as fh:
            fh.write(html_content)
        LOGGER.info("HTML saved to %s", filename)
    except Exception as exc:  # pragma: no cover - defensive logging
        LOGGER.error("Failed to save HTML content to %s: %s", filename, exc)
        raise


def _normalise_year(raw_year) -> str:
    """Return a sortable string representation for a publication year."""
    if raw_year is None:
        return 'N/A'
    if isinstance(raw_year, int):
        return str(raw_year)
    text = str(raw_year).strip()
    return text if text.isdigit() else 'N/A'


def _sorted_years(years: Iterable[str]) -> List[str]:
    def sort_key(value: str) -> Tuple[int, int]:
        if value.isdigit():
            return 0, int(value)
        return 1, 0

    return sorted({year for year in years}, key=sort_key)


def count_items_by_year(papers: Iterable[Dict], patents: Iterable[Dict]):
    """Count how many conference papers, journal papers, and patents were produced per year."""
    conference_count_per_year: Dict[str, int] = {}
    journal_count_per_year: Dict[str, int] = {}
    patent_count_per_year: Dict[str, int] = {}

    papers = papers or []
    patents = patents or []

    for paper in papers:
        bib = paper.get('bib', {})
        year = _normalise_year(bib.get('pub_year'))
        target = journal_count_per_year if bib.get('journal') else conference_count_per_year
        target[year] = target.get(year, 0) + 1

    for patent in patents:
        year = _normalise_year(patent.get('pub_year'))
        patent_count_per_year[year] = patent_count_per_year.get(year, 0) + 1

    all_years = _sorted_years(
        list(conference_count_per_year) + list(journal_count_per_year) + list(patent_count_per_year)
    )

    conference_counts_list = [conference_count_per_year.get(year, 0) for year in all_years]
    journal_counts_list = [journal_count_per_year.get(year, 0) for year in all_years]
    patent_counts_list = [patent_count_per_year.get(year, 0) for year in all_years]

    total_conference_papers = sum(conference_counts_list)
    total_journal_papers = sum(journal_counts_list)
    total_patents = sum(patent_counts_list)

    LOGGER.debug(
        "Computed yearly totals - Years: %s, Conferences: %s, Journals: %s, Patents: %s",
        all_years,
        conference_counts_list,
        journal_counts_list,
        patent_counts_list,
    )

    return (
        conference_counts_list,
        journal_counts_list,
        patent_counts_list,
        all_years,
        total_conference_papers,
        total_journal_papers,
        total_patents,
    )
