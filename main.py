from flask import Flask, render_template, request
from site_content import CAPABILITIES, METRICS, PLANETAIR_WORKFLOW, PROJECTS, SKILL_AREAS, featured_publications, travel_countries

app = Flask(__name__)
SITE_URL = "https://guillaumesabiron.github.io"


@app.context_processor
def global_template_data() -> dict[str, str]:
    """Public, canonical site settings shared by every static page."""
    return {"site_url": SITE_URL}
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
    return render_template(
        'index.html',
        lang=page_language(),
        metrics=METRICS,
        projects=PROJECTS,
        capabilities=CAPABILITIES,
        featured_publications=featured_publications(),
        travel_countries=travel_countries(),
        planetair_workflow=PLANETAIR_WORKFLOW,
    )


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
@app.route('/skills/')
def skills():
    return render_template('skills_page.html', lang=page_language(), capabilities=CAPABILITIES, skill_areas=SKILL_AREAS)

@app.route('/references')
def references():
    return render_section('references.html')

@app.route('/publications/')
def publications():
    return render_template('publications_page.html', lang=page_language())


@app.errorhandler(404)
def not_found(_error):
    return render_template('not_found.html', lang=page_language()), 404

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
