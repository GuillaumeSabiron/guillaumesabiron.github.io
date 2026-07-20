from __future__ import annotations

import shutil
from pathlib import Path

from main import app


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "docs"
STATIC_SRC = PROJECT_ROOT / "static"
STATIC_DEST = OUTPUT_DIR / "static"

def _render_page(client, route: str, language: str, static_prefix: str, replacements: dict[str, str]) -> str:
    rendered = client.get(route, query_string={"lang": language}).get_data(as_text=True)
    rendered = rendered.replace('href="/static/', f'href="{static_prefix}')
    rendered = rendered.replace('src="/static/', f'src="{static_prefix}')
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered


def _static_links(html: str, language: str, depth: int) -> str:
    """Replace Flask query-string navigation with paths that work on Pages."""
    prefix = "../" * depth
    home = prefix or "./"
    french_home = f"{prefix}fr/" if depth == 0 else ("./" if language == "fr" and depth == 1 else f"{prefix}fr/")
    targets = {
        "/?lang=en": home,
        "/?lang=fr": french_home,
        "/skills/?lang=en": f"{prefix}skills/",
        "/skills/?lang=fr": f"{prefix}fr/skills/",
        "/publications/?lang=en": f"{prefix}publications/",
        "/publications/?lang=fr": f"{prefix}fr/publications/",
    }
    # Replace longer paths first: otherwise the home-path pattern is also a
    # substring of `/skills/?lang=…` and produces invalid links.
    for source, target in sorted(targets.items(), key=lambda item: len(item[0]), reverse=True):
        html = html.replace(source, target)
    return html


def build_static_site() -> Path:
    with app.test_client() as client:
        rendered_en = _static_links(_render_page(client, "/", "en", "static/", {}), "en", 0)
        rendered_fr = _static_links(_render_page(client, "/", "fr", "../static/", {}), "fr", 1)
        publications_en = _static_links(_render_page(client, "/publications/", "en", "../static/", {}), "en", 1)
        publications_fr = _static_links(_render_page(client, "/publications/", "fr", "../../static/", {}), "fr", 2)
        skills_en = _static_links(_render_page(client, "/skills/", "en", "../static/", {}), "en", 1)
        skills_fr = _static_links(_render_page(client, "/skills/", "fr", "../../static/", {}), "fr", 2)
        not_found_en = _static_links(_render_page(client, "/missing", "en", "static/", {}), "en", 0)
        not_found_fr = _static_links(_render_page(client, "/missing", "fr", "../static/", {}), "fr", 1)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        STATIC_SRC,
        STATIC_DEST,
        # Historical map libraries are retained in source history only; the
        # Pages output uses the lightweight local map implementation.
        ignore=shutil.ignore_patterns(".DS_Store", "d3.v3.min.js", "topojson.v1.min.js", "datamaps.world.min.js"),
        dirs_exist_ok=True,
    )

    (OUTPUT_DIR / "index.html").write_text(rendered_en, encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT_DIR / "404.html").write_text(not_found_en, encoding="utf-8")
    publications_dir = OUTPUT_DIR / "publications"
    publications_dir.mkdir(exist_ok=True)
    (publications_dir / "index.html").write_text(publications_en, encoding="utf-8")
    french_dir = OUTPUT_DIR / "fr"
    french_dir.mkdir(exist_ok=True)
    (french_dir / "index.html").write_text(rendered_fr, encoding="utf-8")
    (french_dir / "404.html").write_text(not_found_fr, encoding="utf-8")
    french_publications_dir = french_dir / "publications"
    french_publications_dir.mkdir(exist_ok=True)
    (french_publications_dir / "index.html").write_text(publications_fr, encoding="utf-8")
    skills_dir = OUTPUT_DIR / "skills"
    skills_dir.mkdir(exist_ok=True)
    (skills_dir / "index.html").write_text(skills_en, encoding="utf-8")
    french_skills_dir = french_dir / "skills"
    french_skills_dir.mkdir(exist_ok=True)
    (french_skills_dir / "index.html").write_text(skills_fr, encoding="utf-8")
    (OUTPUT_DIR / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://guillaumesabiron.github.io/sitemap.xml\n", encoding="utf-8")
    pages = ["", "fr/", "skills/", "fr/skills/", "publications/", "fr/publications/"]
    sitemap_urls = "\n".join(f"  <url><loc>https://guillaumesabiron.github.io/{page}</loc></url>" for page in pages)
    (OUTPUT_DIR / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>\n', encoding="utf-8")

    return OUTPUT_DIR


if __name__ == "__main__":
    output = build_static_site()
    print(f"Static site generated in {output}")
