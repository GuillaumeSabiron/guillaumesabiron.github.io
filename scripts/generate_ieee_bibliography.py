"""Generate the downloadable IEEE-style publication and patent bibliography."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers_data.json"
OUTPUT_PATH = ROOT / "static" / "documents" / "guillaume-sabiron-publications-patents-ieee.txt"


def _initialise_author(author: str) -> str:
    """Return a compact IEEE-style author name."""
    parts = author.strip().split()
    if len(parts) < 2:
        return author.strip()
    if parts[0].isupper() and not parts[-1].isupper():
        return f"{parts[-1][0]}. {' '.join(parts[:-1]).title()}"
    return f"{' '.join(f'{part[0]}.' for part in parts[:-1])} {parts[-1]}"


def _authors(raw_authors: str) -> str:
    people = [_initialise_author(person) for person in raw_authors.split(" and ") if person.strip()]
    if len(people) < 2:
        return people[0] if people else "G. Sabiron"
    if len(people) == 2:
        return " and ".join(people)
    return ", ".join(people[:-1]) + f", and {people[-1]}"


def _format_publication(paper: dict) -> tuple[int, str]:
    bib = paper["bib"]
    year = int(bib.get("pub_year") or 0)
    venue = bib.get("journal") or bib.get("conference") or bib.get("publisher") or bib.get("citation", "")
    details = []
    if bib.get("volume"):
        details.append(f"vol. {bib['volume']}")
    if bib.get("pages"):
        details.append(f"pp. {bib['pages'].replace('-', '–')}")
    details.append(str(year))
    citation = f'{_authors(bib.get("author", ""))}, “{bib["title"]},” {venue}'
    citation += ", " + ", ".join(details) + "."
    if paper.get("pub_url"):
        citation += f" [Online]. Available: {paper['pub_url']}"
    return year, citation


SUPPLEMENTAL_PUBLICATIONS = [
    (2027, "G. Sabiron, G. De Nunzio, N. Pernet, A. El Feki, and S. Bussod, “Source Apportionment of Pollutant Emissions with PLANET’AIR: A Digital Platform for Enhanced Air Quality Decision-Making,” in EARPA Form Forum 2025, SpringerBriefs in Applied Sciences and Technology, pp. 93–109, 2027, doi: 10.1007/978-3-032-28319-1_7. [Online]. Available: https://doi.org/10.1007/978-3-032-28319-1_7"),
    (2026, "B. Othman and G. Sabiron, “A Multi-resolution Mobility-aware Framework for Dynamic Air Pollution Exposure Assessment,” NetMob 2026, Niterói, Brazil, Oct. 14–16, 2026 (forthcoming conference abstract). [Online]. Available: https://www.netmob.org/www26/"),
    (2025, "G. Sabiron and S. Bussod, “R-TAMS: An innovative decision support tool for real-time and prospective air quality and road traffic emissions monitoring,” in Proceedings of the 2024 Conference on Sustainable Urban Mobility, Springer LNITI, pp. 874–885, 2025, doi: 10.1007/978-3-031-82818-8_66. [Online]. Available: https://doi.org/10.1007/978-3-031-82818-8_66"),
    (2024, "S. Bussod and G. Sabiron, “Deep learning-based method for an assessment of road traffic pollutant estimation from predicted driving behaviors,” in 2024 International Conference on Machine Learning and Applications, 2024, doi: 10.1109/61862.2024.00095. [Online]. Available: https://ieeexplore.ieee.org/document/10903448"),
]


PATENTS = [
    (2026, "G. Sabiron", "Procédé de détermination de la dispersion atmosphérique d’au moins un polluant", "FR3167737A1", "published application", "https://patents.google.com/patent/FR3167737A1/fr"),
    (2026, "G. Sabiron", "Procédé de détermination d’un débit de véhicules sur un réseau routier", "FR3160497B1", "granted patent", "https://patents.google.com/patent/FR3160497B1/fr"),
    (2025, "G. Sabiron", "Procédé de détermination d’une quantité d’au moins un polluant émis par un ensemble de véhicules", "EP4575943A1", "published application", "https://patents.google.com/patent/EP4575943A1/fr"),
    (2025, "G. De Nunzio, G. Sabiron, and L. Thibault", "Procédé de détermination d’émissions polluantes, sonores ou de paramètres de sécurité routière", "EP3836115B1", "granted patent", "https://patents.google.com/patent/EP3836115B1/fr"),
    (2024, "F. J. Gonzalez de Cossio Echeverria, G. De Nunzio, and G. Sabiron", "Procédé de détermination d’au moins un attribut du trafic routier pour un réseau de transport", "FR3145802A1", "published application", "https://patents.google.com/patent/FR3145802A1/fr"),
    (2024, "F. J. Gonzalez de Cossio Echeverria and G. Sabiron", "Procédé de détermination d’un mode de transport d’un trajet parcouru par au moins un utilisateur", "EP4375619A3", "application publication", "https://patents.google.com/patent/EP4375619A3/fr"),
    (2023, "B. Othman, M. Laraki, G. De Nunzio, and G. Sabiron", "Procédé de détermination d’un débit de véhicules sur un réseau routier à partir de données de géolocalisation", "EP4261802A1", "published application", "https://patents.google.com/patent/EP4261802A1/fr"),
    (2023, "F. Guillemin, G. Sabiron, and R. Goussault", "Procédé de détermination des composantes de la vitesse du vent au moyen d’un capteur de télédétection par laser et d’une cohérence temporelle", "EP4172648A1", "published application", "https://patents.google.com/patent/EP4172648A1/fr"),
    (2022, "D. Collet, G. Sabiron, D. Di Domenico, and M. Al-Amir", "Procédé et système de contrôle d’une grandeur d’une éolienne par choix du contrôleur par apprentissage automatique", "EP3956559A1", "published application", "https://patents.google.com/patent/EP3956559A1/fr"),
    (2022, "F. J. Gonzalez de Cossio Echeverria, G. Sabiron, and L. Thibault", "Procédé de caractérisation d’un trajet parcouru par un utilisateur", "EP3936824A1", "published application", "https://patents.google.com/patent/EP3936824A1/fr"),
    (2021, "J. Chauvin, F. Guillemin, R. Goussault, G. Sabiron, and B. Bayon", "Procédé de détermination des composantes de la vitesse du vent au moyen d’un capteur de télédétection par laser", "CA3177085A1", "published application", "https://patents.google.com/patent/CA3177085A1/fr"),
    (2021, "D. Di Domenico, A. Chasse, and G. Sabiron", "Procédé et dispositif de détermination d’une estimation de la masse totale d’un véhicule automobile", "EP3452792B1", "granted patent", "https://patents.google.com/patent/EP3452792B1/fr"),
    (2020, "A. Chasse, D. Di Domenico, and G. Sabiron", "Procédé et dispositif d’analyse de la répartition des dépenses énergétiques d’un véhicule automobile", "EP3515763B1", "granted patent", "https://patents.google.com/patent/EP3515763B1/fr"),
]


def generate_bibliography() -> str:
    data = json.loads(PAPERS_PATH.read_text(encoding="utf-8"))
    records: dict[str, tuple[int, str]] = {}
    for paper in data["papers"]:
        if "patents.google.com" in paper.get("pub_url", ""):
            continue
        title = re.sub(r"\s+", " ", paper["bib"]["title"]).strip().lower()
        records[title] = _format_publication(paper)
    for year, citation in SUPPLEMENTAL_PUBLICATIONS:
        records[citation.split(",”", 1)[0].lower()] = (year, citation)

    lines = [
        "Guillaume Sabiron — Publications and patent portfolio",
        "IEEE-style text export",
        f"Generated from the public portfolio on {date.today().isoformat()}.",
        "",
        "PUBLICATIONS",
    ]
    for index, (_, citation) in enumerate(sorted(records.values(), key=lambda item: (-item[0], item[1])), start=1):
        lines.append(f"[{index}] {citation}")
    lines.extend(["", "PATENTS AND PATENT APPLICATIONS"])
    for index, (year, authors, title, number, status, url) in enumerate(sorted(PATENTS, reverse=True), start=1):
        lines.append(f"[P{index}] {authors}, “{title},” {number}, {status}, {year}. [Online]. Available: {url}")
    lines.append("")
    return "\n".join(lines)


def write_bibliography(destination: Path = OUTPUT_PATH) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(generate_bibliography(), encoding="utf-8")
    return destination


if __name__ == "__main__":
    print(f"IEEE bibliography generated in {write_bibliography()}")
