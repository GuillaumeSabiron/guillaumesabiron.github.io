# Guillaume Sabiron — professional portfolio

Bilingual Flask and static portfolio presenting R&D leadership, applied AI, scientific systems, digital products, mobility and environmental intelligence. The homepage is narrative and project-led; detailed **Skills** and **Publications** pages provide supporting depth.

## Live website

The public portfolio is available at:

<https://guillaumesabiron.github.io/>

GitHub Pages deploys the static site automatically after every push to `main`.

## Local development

```bash
./.venv/bin/python main.py
```

Open `http://127.0.0.1:5000` (French: `http://127.0.0.1:5000/?lang=fr`).

## Build and checks

```bash
./.venv/bin/python -m compileall main.py build_static.py site_content.py utils scripts
./.venv/bin/python build_static.py
./.venv/bin/python scripts/check_site.py
npm run build
npm run quality
```

`build_static.py` generates the GitHub Pages output in `docs/`; `npm run build` packages it in `dist/`. Generated directories must never be edited directly.

`npm run quality` is the routine to run before a content or design update: it compiles the Python sources, regenerates the public site, checks every static page, and packages the deployment artifact. GitHub Actions runs the same checks on every push to `main`.

## Privacy

The bilingual [privacy policy](https://guillaumesabiron.github.io/privacy/) documents the contact form (Formspree), Cloudflare Web Analytics, aggregated CV-download metrics and third-party media loaded after an explicit click.

## Content sources

- `site_content.py` — public metrics, selected projects, capabilities and selected publications.
- `Guillaume_Sabiron_data.json` — publication source data.
- `data/travel_countries.json` — sole source for the personal travel summary.
- `static/img/projects/` — optimised conceptual project illustrations (AVIF).
- `static/documents/` — public French and English CV PDFs.
- `templates/` — page shells and presentation only.

To add a project, define its bilingual text, image alt text, public links and image path in `site_content.py`; then add the optimised image under `static/img/projects/`. Do not describe conceptual illustrations as product screenshots or experimental results.

## Architecture

- Flask and Jinja for local rendering
- native HTML, CSS and JavaScript
- static export in `docs/`
- no frontend framework or database; the travel map is a lightweight local SVG-style interaction

GitHub Actions runs static checks and deploys GitHub Pages on pushes to `main`.

## Automated quality and monitoring

Install test dependencies with `npm ci` and browsers with
`npx playwright install chromium webkit`, then run `npm run quality:full`.
This checks internal links and anchors, SEO values, reciprocal language links,
the sitemap, Worker request semantics, keyboard navigation, mobile layout and
automatically detectable WCAG A/AA issues with axe. Chromium desktop/mobile and
WebKit mobile are tested in both languages. Automated tests do not certify full
accessibility or verify that an external publication link targets the right paper.

GitHub Pages deployment now waits for this suite. A separate weekly Monday
07:00 UTC run checks the repository; failures and browser reports are available
in GitHub Actions. No test events are sent to production analytics or Formspree.

See [monitoring setup](docs-monitoring.md) for daily visits, page views and CV
requests. Updating the Cloudflare Worker is a separate deployment from Pages.

## Search engines

The static build generates canonical URLs, reciprocal language alternatives, `sitemap.xml`, `robots.txt` and an Open Graph image. Submit `https://guillaumesabiron.github.io/sitemap.xml` in [Google Search Console](https://search.google.com/search-console/) and [Bing Webmaster Tools](https://www.bing.com/webmasters/), then validate the public home page with Google’s Rich Results Test. Do not add verification tokens to the repository unless they are issued for this domain.

## Before publication

Confirm public links, email address, CV versions, project names, videos and quantitative claims. The project illustrations are conceptual; values visible inside them are not asserted as portfolio results.
