import scholarly
import requests
from bs4 import BeautifulSoup
import json
import html
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s - Line: %(lineno)d')

# Extract author data from Google Scholar
def extract_google_scholar(author_name):
    logging.info(f"Searching for author: {author_name}")
    try:
        search_query = scholarly.search_author(author_name)
        author = next(search_query)
        logging.info(f"Author found: {author['name']}")
    except StopIteration:
        logging.error(f"No author found with the name {author_name}")
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
            logging.error(f"Error processing paper: {str(e)}")
            continue

    return papers


# Extract patents from Google Patents
def extract_google_patents(author_name):
    logging.info(f"Searching for patents for: {author_name}")
    query_url = f"https://patents.google.com/?q={author_name.replace(' ', '+')}"
    print(query_url)
    try:
        response = requests.get(query_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print(response)
        print(soup)
        # Parse patents
        patents = []
        for result in soup.find_all('tr', class_='result'):
            patent_title = result.find('span', class_='title').get_text(strip=True)
            patent_number = result.find('td', class_='publication').get_text(strip=True)
            pub_date = result.find('td', class_='publication').get_text(strip=True)

            patents.append({
                'title': patent_title,
                'number': patent_number,
                'pub_year': pub_date[:4] if pub_date else 'N/A'
            })

        logging.info(f"Found {len(patents)} patents")
        return patents

    except Exception as e:
        logging.error(f"Error fetching patents: {str(e)}")
        return []

# Save papers and patents data to a JSON file
def save_data_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save JSON data: {str(e)}")

# Load papers and patents data from JSON file
def load_json_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            logging.info(f"Loaded {len(content)} characters from {filename}")
            return json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        logging.error(f"Error loading JSON data: {str(e)}")
        raise


# Count papers, patents per year (separately for journals, conferences, patents)
def count_items_by_year(papers, patents):
    conference_count_per_year = {}
    journal_count_per_year = {}
    patent_count_per_year = {}

    # Count papers
    for paper in papers:
        bib = paper.get('bib', {})
        year = bib.get('pub_year', 'N/A')

        if 'journal' in bib:
            journal_count_per_year[year] = journal_count_per_year.get(year, 0) + 1
        else:
            conference_count_per_year[year] = conference_count_per_year.get(year, 0) + 1

    # Count patents
    for patent in patents:
        year = patent.get('pub_year', 'N/A')
        patent_count_per_year[year] = patent_count_per_year.get(year, 0) + 1

    # Ensure all years have values
    all_years = set(conference_count_per_year.keys()).union(journal_count_per_year.keys()).union(
        patent_count_per_year.keys())
    conference_counts_list = [conference_count_per_year.get(year, 0) for year in sorted(all_years)]
    journal_counts_list = [journal_count_per_year.get(year, 0) for year in sorted(all_years)]
    patent_counts_list = [patent_count_per_year.get(year, 0) for year in sorted(all_years)]

    # Total sums
    total_conference_papers = sum(conference_counts_list)
    total_journal_papers = sum(journal_counts_list)
    total_patents = sum(patent_counts_list)

    return conference_counts_list, journal_counts_list, patent_counts_list, sorted(
        all_years), total_conference_papers, total_journal_papers, total_patents


# Generate HTML for publication list
def generate_html(papers):
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
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #3498db; }}
            .subheading {{ font-size: 1.2em; margin-top: 30px; color: #2c3e50; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 10px; }}
            .description {{ display: none; }}
            .paper a {{ color: #e74c3c; text-decoration: none; cursor: pointer; }}
            .paper a:hover {{ text-decoration: underline; }}
        </style>
        <script>
            function toggleDescription(id) {{
                var element = document.getElementById(id);
                if (element.style.display === 'none') {{
                    element.style.display = 'block';
                }} else {{
                    element.style.display = 'none';
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Publications</h1>

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

    paper_template = """
        <li>
            <a class="reference-title" href="javascript:void(0);" onclick="toggleDescription('{id}')">{title}</a>
            <div class="description" id="{id}" style="display: none;">
                <p><strong>Date:</strong> {year}</p>
                <p><strong>Authors:</strong> {authors}</p>
                <p><strong>Abstract:</strong> {abstract}</p>
                <p><a href="{link}" target="_blank">View Paper</a></p>
            </div>
        </li>
    """

    journal_entries = []
    conference_entries = []
    journal_count = 1
    conference_count = 1

    for paper in papers:
        bib = paper.get('bib', {})
        authors = bib.get('author', 'N/A').replace(' and ', ', ')
        paper_type = bib.get('venue', 'N/A').lower()

        paper_entry = paper_template.format(
            id=f"journal{journal_count}" if 'journal' in paper_type else f"conference{conference_count}",
            title=html.escape(bib.get('title', 'N/A')),
            year=html.escape(str(bib.get('pub_year', 'N/A'))),
            authors=html.escape(authors),
            abstract=html.escape((bib.get('abstract', '')[:200] + '...') if bib.get('abstract') else 'N/A'),
            link=html.escape(paper.get('pub_url', '#'))
        )

        if 'journal' in paper_type:
            journal_entries.append(paper_entry)
            journal_count += 1
        else:
            conference_entries.append(paper_entry)
            conference_count += 1

    return html_template.format(
        journal_entries='\n'.join(journal_entries),
        conference_entries='\n'.join(conference_entries)
    )


# Save the HTML output
def save_html(html_content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"HTML file saved as {filename}")
    except Exception as e:
        logging.error(f"Failed to save HTML file: {str(e)}")


# Main execution
def main():
    json_filename = 'data/papers_data.json'
    html_filename = 'data/papers_list.html'

    author_name = "Guillaume Sabiron"

    try:
        papers = load_json_data(json_filename).get('papers', [])

        # Remove papers where the citation contains "US Patent App."
        papers = [paper for paper in papers if "US Patent App." not in paper.get("bib", {}).get("citation", "")]

        logging.info(f"Loaded {len(papers)} papers from {json_filename}")

        # patents = extract_google_patents(author_name)
        patents = []
        # Save papers and patents to JSON
        filename = f"{author_name.replace(' ', '_')}_data.json"
        save_data_to_json({'papers': papers, 'patents': patents}, filename)

        # Count publications and patents per year
        conference_counts, journal_counts, patent_counts, years, total_conference_papers, total_journal_papers, total_patents = count_items_by_year(
            papers, patents)

        # Log paper counts and totals
        logging.info(f"Years: {years}")
        logging.info(f"Conference papers per year: {conference_counts}")
        logging.info(f"Journal papers per year: {journal_counts}")
        logging.info(f"Patents per year: {patent_counts}")
        logging.info(f"Total conference papers: {total_conference_papers}")
        logging.info(f"Total journal papers: {total_journal_papers}")
        logging.info(f"Total patents papers: {total_patents}")

        # Generate and save HTML
        html_content = generate_html(papers)
        save_html(html_content, html_filename)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
