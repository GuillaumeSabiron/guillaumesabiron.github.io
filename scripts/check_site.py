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
    pages = [root / "index.html", root / "fr" / "index.html", root / "publications" / "index.html", root / "fr" / "publications" / "index.html"]
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
        if "<title>" not in html or 'name="description"' not in html:
            errors.append(f"{page.relative_to(root)}: missing title or description")
    if errors:
        print("Static-site checks failed:", *errors, sep="\n- ")
        return 1
    print(f"Static-site checks passed ({len(pages)} pages).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
