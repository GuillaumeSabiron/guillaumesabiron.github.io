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


def build_static_site() -> Path:
    with app.test_client() as client:
        index_html = client.get("/").get_data(as_text=True)

        soup = BeautifulSoup(index_html, "html.parser")

        for target_id, route in SECTION_ROUTES.items():
            target = soup.find(id=target_id)
            if target is None:
                raise ValueError(f"Missing target container: {target_id}")

            fragment_html = client.get(route).get_data(as_text=True)
            target.clear()
            for node in _fragment_nodes(fragment_html):
                target.append(node)

        for script in soup.find_all("script"):
            script_text = script.get_text(strip=False)
            if "fetch('/expertise')" in script_text or "fetch(\"/expertise\")" in script_text:
                script.decompose()

        init_script = soup.new_tag("script")
        init_script.string = """
document.addEventListener('DOMContentLoaded', function () {
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
        rendered = rendered.replace('href="/static/', 'href="static/')
        rendered = rendered.replace('src="/static/', 'src="static/')

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        STATIC_SRC,
        STATIC_DEST,
        ignore=shutil.ignore_patterns(".DS_Store"),
        dirs_exist_ok=True,
    )

    (OUTPUT_DIR / "index.html").write_text(rendered, encoding="utf-8")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT_DIR / "404.html").write_text(rendered, encoding="utf-8")

    return OUTPUT_DIR


if __name__ == "__main__":
    output = build_static_site()
    print(f"Static site generated in {output}")
