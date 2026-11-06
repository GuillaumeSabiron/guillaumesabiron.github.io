"""Offline internal-link, SEO-value and sitemap checks for the static export."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "docs"
ORIGIN = "https://guillaumesabiron.github.io"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.meta, self.canonicals, self.alternates = set(), [], {}, [], {}
        self.ld, self.json_ld = False, []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "meta":
            self.meta[a.get("name", a.get("property", ""))] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag == "link" and a.get("rel") == "alternate":
            self.alternates[a.get("hreflang")] = a.get("href")
        for key in (("href",) if tag in {"a", "link"} else ("src",) if tag in {"img", "script", "source"} else ()):
            if a.get(key):
                self.links.append(a[key])
        if tag == "script" and a.get("type") == "application/ld+json":
            self.ld = True

    def handle_data(self, data):
        if self.ld:
            self.json_ld.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self.ld = False


def main():
    pages = {p: Page(p.read_text(encoding="utf-8")) for p in ROOT.rglob("*.html")}
    errors = []
    def target(url):
        path = ROOT / unquote(urlsplit(url).path).lstrip("/")
        return path / "index.html" if path.is_dir() else path
    for path, page in pages.items():
        relative = path.relative_to(ROOT).as_posix()
        public_path = "/" + relative.removesuffix("index.html") if path.name == "index.html" else "/" + relative
        current = ORIGIN + public_path
        for link in page.links:
            url = urlsplit(urljoin(current, link))
            if url.scheme not in {"http", "https"} or url.netloc != urlsplit(ORIGIN).netloc:
                continue
            dest = target(url.geturl())
            if not dest.is_file():
                errors.append(f"{relative}: missing internal target {link}")
            elif url.fragment and dest in pages and unquote(url.fragment) not in pages[dest].ids:
                errors.append(f"{relative}: missing anchor {link}")
        if path.name != "404.html":
            if page.canonicals != [current]:
                errors.append(f"{relative}: canonical must equal {current}")
            if page.meta.get("og:url") != current:
                errors.append(f"{relative}: og:url differs from canonical")
            if not page.meta.get("description", "").strip():
                errors.append(f"{relative}: empty description")
            for language in ("fr", "en"):
                alternate = page.alternates.get(language, "")
                dest = target(alternate)
                if not alternate.startswith(ORIGIN + "/") or dest not in pages:
                    errors.append(f"{relative}: invalid {language} alternate")
                elif current not in pages[dest].alternates.values():
                    errors.append(f"{relative}: non-reciprocal {language} alternate")
        for raw in page.json_ld:
            try:
                json.loads(raw)
                if "&amp;" in raw or "&#" in raw:
                    errors.append(f"{relative}: HTML entities inside JSON-LD")
            except ValueError:
                errors.append(f"{relative}: invalid JSON-LD")
    sitemap = ET.parse(ROOT / "sitemap.xml")
    urls = [node.text for node in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    expected = {ORIGIN + "/" + p.relative_to(ROOT).as_posix().removesuffix("index.html") for p in pages if p.name == "index.html"}
    if set(urls) != expected or len(urls) != len(set(urls)):
        errors.append("sitemap: missing, duplicate or unexpected URLs")
    text_sitemap = ROOT / "sitemap.txt"
    if not text_sitemap.is_file() or text_sitemap.read_text(encoding="utf-8").splitlines() != urls:
        errors.append("sitemap.txt: must list the same URLs as sitemap.xml, one per line")
    if errors:
        print("Integrity checks failed:\n- " + "\n- ".join(errors))
        return 1
    print(f"Internal links, anchors, SEO values and sitemap passed ({len(pages)} pages).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
