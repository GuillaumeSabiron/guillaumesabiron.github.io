# Guillaume Sabiron — professional website

This repository contains Guillaume Sabiron&rsquo;s professional website: an English-language digital CV and portfolio for R&amp;D leadership, applied AI, data products, connected mobility, and air quality.

The existing architecture is intentionally lightweight: Flask and Jinja fragments for local development, then a static export for deployment. No frontend framework or database is required.

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

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000). If that port is already in use, Flask can be started on another port, for example:

```bash
./.venv/bin/python -c "from main import app; app.run(debug=True, port=5001)"
```

## Static export for deployment

Generate the static site used by GitHub Pages:

```bash
./.venv/bin/python build_static.py
```

This command rebuilds:

- `docs/index.html`
- `docs/404.html`
- `docs/fr/index.html` and `docs/fr/404.html` (French version)
- `docs/static/`

The live Flask site is English by default; append `?lang=fr` for French. The
static export exposes the same version at `/fr/`. Scientific publication titles
and abstracts stay in their original publication language.

## Deployment build

Build the deployable package only after the static export has been generated:

```bash
npm run build
```

The command prepares:

- `dist/site/` — static site assets
- `dist/server/index.js` — fallback handler for static hosting
- `dist/.openai/hosting.json` — hosting configuration

## Verification commands

The repository does not currently define lint or test scripts. The following checks are available:

```bash
./.venv/bin/python -m compileall main.py build_static.py utils
./.venv/bin/python build_static.py
npm run build
```

## Project structure

- `main.py` — Flask entry point
- `templates/index.html` — single-page shell, navigation, hero, SEO metadata, and fragment loading
- `templates/` — section content for experience, projects, education, skills, publications, positioning, and recognition
- `static/` — CSS, JavaScript, and image assets
- `build_static.py` — static export builder for GitHub Pages
- `docs/` — generated deployment output
- `scripts/build-static-site.mjs` — deployment-package builder
- `utils/`, `data/` — publication helpers and cached source data

## Updating content

- Update the professional profile and navigation in `templates/index.html`. Keep
  the English and French Jinja variants aligned when changing visitor-facing copy.
- Update experience, projects, education, skills, and availability in their corresponding file under `templates/`.
- Update the curated public publication list in `templates/references.html`.
- Use `extract_paper_patent.py` only to regenerate the legacy cached publication list from `data/papers_data.json`; it is not the source of the curated website copy.
- Add images in `static/img/`. The static export copies these assets into `docs/static/img/`.

Generated files in `docs/` and `dist/` should not be edited directly: update the source files first, then rebuild.

## Before public deployment

Confirm that public links, the professional email address, any project names, and quantitative claims are approved for publication. A CV download button should be added only once the corresponding PDF exists in `static/`.
