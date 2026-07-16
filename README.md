# Guillaume Sabiron — personal website

This repository contains Guillaume Sabiron's personal website source code.

The project keeps a Flask version for local development and a static export for GitHub Pages deployment.

## Local development

Create and activate the local virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the site locally:

```bash
./.venv/bin/python main.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Static export for deployment

Generate the static site used by GitHub Pages:

```bash
./.venv/bin/python build_static.py
```

This command rebuilds:

- `docs/index.html`
- `docs/404.html`
- `docs/static/`

## Project structure

- `main.py` — Flask entry point
- `templates/` — HTML templates and content sections
- `static/` — CSS, JavaScript, and image assets
- `build_static.py` — static export builder for GitHub Pages
- `docs/` — generated deployment output
- `utils/`, `data/` — helper scripts and data sources used by the site
