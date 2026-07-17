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


def build_static_site() -> Path:
    with app.test_client() as client:
        rendered_en = _render_page(client, "/", "en", "static/", {'href="/?lang=en"': 'href="./"', 'href="/?lang=fr"': 'href="fr/"', 'href="/publications/?lang=en"': 'href="publications/"', 'href="/publications/?lang=fr"': 'href="fr/publications/"'})
        rendered_fr = _render_page(client, "/", "fr", "../static/", {'href="/?lang=en"': 'href="../"', 'href="/?lang=fr"': 'href="./"', 'href="/publications/?lang=en"': 'href="../publications/"', 'href="/publications/?lang=fr"': 'href="publications/"'})
        publications_en = _render_page(client, "/publications/", "en", "../static/", {'href="/?lang=en"': 'href="../"', 'href="/?lang=fr"': 'href="../fr/"', 'href="/publications/?lang=en"': 'href="./"', 'href="/publications/?lang=fr"': 'href="../fr/publications/"'})
        publications_fr = _render_page(client, "/publications/", "fr", "../../static/", {'href="/?lang=en"': 'href="../../"', 'href="/?lang=fr"': 'href="../"', 'href="/publications/?lang=en"': 'href="../../publications/"', 'href="/publications/?lang=fr"': 'href="./"'})

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        STATIC_SRC,
        STATIC_DEST,
        ignore=shutil.ignore_patterns(".DS_Store"),
        dirs_exist_ok=True,
    )

    (OUTPUT_DIR / "index.html").write_text(rendered_en, encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT_DIR / "404.html").write_text(rendered_en, encoding="utf-8")
    publications_dir = OUTPUT_DIR / "publications"
    publications_dir.mkdir(exist_ok=True)
    (publications_dir / "index.html").write_text(publications_en, encoding="utf-8")
    french_dir = OUTPUT_DIR / "fr"
    french_dir.mkdir(exist_ok=True)
    (french_dir / "index.html").write_text(rendered_fr, encoding="utf-8")
    (french_dir / "404.html").write_text(rendered_fr, encoding="utf-8")
    french_publications_dir = french_dir / "publications"
    french_publications_dir.mkdir(exist_ok=True)
    (french_publications_dir / "index.html").write_text(publications_fr, encoding="utf-8")

    return OUTPUT_DIR


if __name__ == "__main__":
    output = build_static_site()
    print(f"Static site generated in {output}")
