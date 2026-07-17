from __future__ import annotations

from typing import Dict, Iterable, List

def generate_html_header(total_counts: Dict[str, int]) -> str:
    """Generates the HTML header with total counts."""
    header = f"""
    <h1>Publications</h1>
    <p>Total Journal Papers: {total_counts['journal']}</p>
    <p>Total Conference Papers: {total_counts['conference']}</p>
    <p>Total Patents: {total_counts['patents']}</p>
    """
    return header

def generate_paper_entries(papers: Iterable[Dict]) -> str:
    """Generates HTML entries for each paper."""
    entries: List[str] = []
    for index, paper in enumerate(papers, start=1):
        bib = paper.get('bib', {})
        authors = bib.get('author', '')
        if isinstance(authors, str):
            authors = authors.replace(' and ', ', ')
        else:
            authors = ', '.join(authors) if isinstance(authors, (list, tuple)) else 'N/A'

        paper_id = paper.get('id') or paper.get('pub_url') or f"paper-{index}"

        entries.append(
            f"""
        <li>
            <a class="reference-title" href="javascript:void(0);" onclick="toggleDescription('{paper_id}')">{bib.get('title', 'N/A')}</a>
            <div class="description" id="{paper_id}" style="display: none;">
                <p><strong>Date:</strong> {bib.get('pub_year', 'N/A')}</p>
                <p><strong>Authors:</strong> {authors}</p>
                <p><strong>Abstract:</strong> {bib.get('abstract', 'N/A')}</p>
                <p><a href="{paper.get('pub_url', '#')}" target="_blank">View Paper</a></p>
            </div>
        </li>
        """
        )
    return ''.join(entries)

def generate_html(papers: List[Dict], total_counts: Dict[str, int]) -> str:
    """Generates the full HTML content."""
    papers = sorted(
        papers,
        key=lambda paper: int(str(paper.get('bib', {}).get('pub_year', '')).strip())
        if str(paper.get('bib', {}).get('pub_year', '')).strip().isdigit() else 0,
        reverse=True,
    )
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Publications</title>
        <style>
            /* Styles here... */
        </style>
        <script>
            function toggleDescription(id) {
                var element = document.getElementById(id);
                if (element.style.display === 'none') {
                    element.style.display = 'block';
                } else {
                    element.style.display = 'none';
                }
            }
        </script>
    </head>
    <body>
        {header}
        <div class="subheading">Journals</div>
        <ul>
            {journal_entries}
        </ul>
        <div class="subheading">Conferences</div>
        <ul>
            {conference_entries}
        </ul>
    </body>
    </html>
    """

    header = generate_html_header(total_counts)

    journal_entries = ""
    conference_entries = ""
    for paper in papers:
        bib = paper.get('bib', {})
        paper_type = bib.get('venue', 'N/A').lower()

        entry = generate_paper_entries([paper])  # Generate entry for the current paper
        if 'journal' in paper_type:
            journal_entries += entry
        else:
            conference_entries += entry

    return html_template.format(
        header=header,
        journal_entries=journal_entries,
        conference_entries=conference_entries
    )
