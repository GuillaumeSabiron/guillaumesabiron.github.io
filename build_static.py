from __future__ import annotations

import shutil
from pathlib import Path

from bs4 import BeautifulSoup

from main import app


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "docs"
STATIC_SRC = PROJECT_ROOT / "static"
STATIC_DEST = OUTPUT_DIR / "static"

SECTION_ROUTES = {
    "expertise-content": "/expertise",
    "projects-content": "/projects",
    "experience-content": "/experience",
    "education-content": "/education",
    "skills-content": "/skills",
    "references-content": "/references",
    "interests-content": "/interests",
    "awards-content": "/awards",
    "charts-content": "/charts",
    "footer": "/footer",
}


def _fragment_nodes(fragment_html: str):
    fragment_soup = BeautifulSoup(fragment_html, "html.parser")
    return list(fragment_soup.contents)


def _render_page(client, language: str, static_prefix: str, language_links: dict[str, str]) -> str:
    index_html = client.get("/", query_string={"lang": language}).get_data(as_text=True)

    soup = BeautifulSoup(index_html, "html.parser")

    for target_id, route in SECTION_ROUTES.items():
        target = soup.find(id=target_id)
        if target is None:
            raise ValueError(f"Missing target container: {target_id}")

        fragment_html = client.get(route, query_string={"lang": language}).get_data(as_text=True)
        target.clear()
        for node in _fragment_nodes(fragment_html):
            target.append(node)

    for script in soup.find_all("script"):
        script_text = script.get_text(strip=False)
        if "fetch(withLanguage('/expertise'))" in script_text:
            script.decompose()

    init_script = soup.new_tag("script")
    init_script.string = """
document.addEventListener('DOMContentLoaded', function () {
    if (typeof window.initializePublicationList === 'function') {
        window.initializePublicationList();
    }
    if (typeof window.initializeMap === 'function') {
        window.initializeMap();
    }
    if (typeof window.initializeChart === 'function') {
        window.initializeChart();
    }
});
""".strip()
    soup.body.append(init_script)

    rendered = str(soup)
    rendered = rendered.replace('href="/static/', f'href="{static_prefix}')
    rendered = rendered.replace('src="/static/', f'src="{static_prefix}')
    for language_code, href in language_links.items():
        rendered = rendered.replace(f'href="/?lang={language_code}"', f'href="{href}"')
    return rendered


def build_static_site() -> Path:
    with app.test_client() as client:
        rendered_en = _render_page(
            client, "en", "static/", {"en": "./", "fr": "fr/"}
        )
        rendered_fr = _render_page(
            client, "fr", "../static/", {"en": "../", "fr": "./"}
        )

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
    french_dir = OUTPUT_DIR / "fr"
    french_dir.mkdir(exist_ok=True)
    (french_dir / "index.html").write_text(rendered_fr, encoding="utf-8")
    (french_dir / "404.html").write_text(rendered_fr, encoding="utf-8")

    return OUTPUT_DIR


if __name__ == "__main__":
    output = build_static_site()
    print(f"Static site generated in {output}")
