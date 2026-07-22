"""Small, dependency-free checks for the generated static site."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path


class Audit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.h1_count = 0
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and not values.get("alt"):
            self.errors.append("image without alt text")
        if values.get("target") == "_blank" and values.get("rel") != "noopener noreferrer":
            self.errors.append("external target without noopener noreferrer")


def main() -> int:
    root = Path(__file__).resolve().parents[1] / "docs"
    pages = [
        root / "index.html",
        root / "fr" / "index.html",
        root / "publications" / "index.html",
        root / "fr" / "publications" / "index.html",
        root / "skills" / "index.html",
        root / "fr" / "skills" / "index.html",
        root / "404.html",
        root / "fr" / "404.html",
    ]
    english_pages = {root / "index.html", root / "skills" / "index.html", root / "publications" / "index.html"}
    french_pages = {root / "fr" / "index.html", root / "fr" / "skills" / "index.html", root / "fr" / "publications" / "index.html"}
    errors: list[str] = []
    for page in pages:
        if not page.exists():
            errors.append(f"missing generated page: {page.relative_to(root)}")
            continue
        html = page.read_text(encoding="utf-8")
        audit = Audit()
        audit.feed(html)
        duplicated = {item for item in audit.ids if audit.ids.count(item) > 1}
        if duplicated:
            errors.append(f"{page.relative_to(root)}: duplicate IDs {sorted(duplicated)}")
        if audit.h1_count != 1:
            errors.append(f"{page.relative_to(root)}: expected one h1, got {audit.h1_count}")
        errors.extend(f"{page.relative_to(root)}: {item}" for item in audit.errors)
        if "YYYY-MM" in html or "lorem ipsum" in html.lower():
            errors.append(f"{page.relative_to(root)}: contains placeholder text")
        if "skills-scroll" in html or "publication-carousel" in html:
            errors.append(f"{page.relative_to(root)}: contains retired animated component")
        if "<title>" not in html or 'name="description"' not in html:
            errors.append(f"{page.relative_to(root)}: missing title or description")
        expected_lang = "fr" if page in french_pages or page == root / "fr" / "404.html" else "en"
        if f'<html lang="{expected_lang}">' not in html:
            errors.append(f"{page.relative_to(root)}: incorrect document language")
        if page not in {root / "404.html", root / "fr" / "404.html"}:
            for required in ('rel="canonical"', 'property="og:url"', 'property="og:image"', 'property="og:image:alt"', 'name="twitter:card"', 'name="twitter:title"', 'name="twitter:description"', 'hreflang="en"', 'hreflang="fr"'):
                if required not in html:
                    errors.append(f"{page.relative_to(root)}: missing SEO metadata {required}")
            if 'https://guillaumesabiron.github.io' not in html:
                errors.append(f"{page.relative_to(root)}: SEO URLs are not absolute")
        if page in english_pages and (">Conférences<" in html or "Retour au site" in html):
            errors.append(f"{page.relative_to(root)}: contains French UI label")
        if page in french_pages and (">Conferences<" in html or "Back to site" in html):
            errors.append(f"{page.relative_to(root)}: contains English UI label")
        if '?lang=' in html:
            errors.append(f"{page.relative_to(root)}: query-string language link remains")
        if '<ul></ul>' in html:
            errors.append(f"{page.relative_to(root)}: empty list remains")
        if "static.cloudflareinsights.com/beacon.min.js" not in html:
            errors.append(f"{page.relative_to(root)}: missing analytics beacon")
    required_assets = [
        root / "static" / "documents" / "guillaume-sabiron-cv-en.pdf",
        root / "static" / "documents" / "guillaume-sabiron-cv-fr.pdf",
        root / "static" / "img" / "projects" / "planetair-project.avif",
        root / "static" / "img" / "projects" / "geco-air-project.avif",
        root / "static" / "img" / "projects" / "wec-control-project.avif",
        root / "static" / "img" / "projects" / "phd-lunar-landing-project.avif",
    ]
    errors.extend(f"missing generated asset: {asset.relative_to(root)}" for asset in required_assets if not asset.exists())
    for asset in (root / "robots.txt", root / "sitemap.xml", root / "static" / "img" / "og-guillaume-sabiron.png"):
        if not asset.exists():
            errors.append(f"missing generated SEO asset: {asset.relative_to(root)}")
    if errors:
        print("Static-site checks failed:", *errors, sep="\n- ")
        return 1
    print(f"Static-site checks passed ({len(pages)} pages).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
