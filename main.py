import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent


def carousel_publications() -> list[dict[str, str | int]]:
    """Expose only verified title/year metadata for the homepage carousel."""
    source = json.loads((PROJECT_ROOT / "Guillaume_Sabiron_data.json").read_text(encoding="utf-8"))
    publications = []
    for item in source.get("papers", []):
        bib = item.get("bib", {})
        title, year = bib.get("title"), bib.get("pub_year")
        if title and year:
            publications.append({"title": title, "year": year})
    return sorted(publications, key=lambda item: item["year"], reverse=True)


def page_language() -> str:
    """Return the supported language requested by the visitor.

    Keeping the language in the query string makes the Flask fragments and the
    statically exported /fr/ page use the exact same templates.
    """
    return "fr" if request.args.get("lang") == "fr" else "en"


def render_section(template_name: str):
    return render_template(template_name, lang=page_language())

@app.route('/')
def home():
    return render_template('index.html', lang=page_language(), carousel_papers=carousel_publications())


@app.route('/header')
def header():
    return render_section('header.html')

@app.route('/experience')
def experience():
    return render_section('experience.html')

@app.route('/expertise')
def expertise():
    return render_section('expertise.html')

@app.route('/projects')
def projects():
    return render_section('projects.html')

@app.route('/education')
def education():
    return render_section('education.html')

@app.route('/skills')
def skills():
    return render_section('skills.html')

@app.route('/references')
def references():
    return render_section('references.html')

@app.route('/publications/')
def publications():
    return render_template('publications_page.html', lang=page_language())

@app.route('/interests')
def interests():
    return render_section('interests.html')

@app.route('/awards')
def awards():
    return render_section('awards.html')

@app.route('/footer')
def footer():
    return render_section('footer.html')

if __name__ == '__main__':
    app.run(debug=True)
