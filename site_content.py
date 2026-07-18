"""Public portfolio content kept separate from page templates."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent

METRICS = [
    {"value": "15", "en": "years in applied research, engineering and innovation", "fr": "ans en recherche appliquée, ingénierie et innovation"},
    {"value": "20+", "en": "multidisciplinary contributors coordinated annually", "fr": "contributeurs pluridisciplinaires coordonnés chaque année", "note_en": "Functional coordination across internal and external teams, engineers, PhD candidates and contractors.", "note_fr": "Coordination fonctionnelle d’équipes internes et externes, d’ingénieurs, doctorants et prestataires."},
    {"value": "70k+", "en": "users reached through Geco Air", "fr": "utilisateurs touchés via Geco Air"},
    {"value": "80M+", "en": "kilometres analysed", "fr": "kilomètres analysés"},
]

CAPABILITIES = [
    {"title": {"en": "Science & Systems", "fr": "Science et systèmes"}, "items": {"en": ["Systems architecture", "Problem framing", "Applied AI", "Physical and hybrid modelling", "Complex-system integration", "Geospatial and environmental modelling"], "fr": ["Architecture de systèmes", "Cadrage de problèmes", "IA appliquée", "Modélisation physique et hybride", "Intégration de systèmes complexes", "Modélisation géospatiale et environnementale"]}},
    {"title": {"en": "Products & Technology", "fr": "Produits et technologie"}, "items": {"en": ["Scientific products", "Data platforms", "Product roadmaps", "Decision-support systems", "APIs and digital services", "Research-to-product execution"], "fr": ["Produits scientifiques", "Plateformes data", "Feuilles de route produit", "Systèmes d’aide à la décision", "API et services numériques", "Passage de la recherche au produit"]}},
    {"title": {"en": "Leadership & Collaboration", "fr": "Leadership et collaboration"}, "items": {"en": ["R&D program leadership", "Cross-functional coordination", "Technical decision-making", "Partner alignment", "Scientific communication", "International collaboration"], "fr": ["Pilotage de programmes R&D", "Coordination transversale", "Décision technique", "Alignement des partenaires", "Communication scientifique", "Collaboration internationale"]}},
]

PROJECTS = [
    {
        "id": "planetair", "featured": True, "image": "img/projects/planetair-project.avif", "logo": "img/planetair-logo.png", "width": 1600, "height": 900,
        "label": "PLANET’AIR", "url": "https://www.planet-ifpen.cloud/planet-air", "video": "https://www.youtube-nocookie.com/embed/sOS96pJV72E",
        "title": {"en": "From scientific models to a territorial decision platform", "fr": "Des modèles scientifiques à une plateforme de décision territoriale"},
        "summary": {"en": "PLANET’AIR turns mobility, traffic and fleet data into road-emission, noise and air-quality indicators for territorial scenario analysis.", "fr": "PLANET’AIR transforme des données de mobilité, de trafic et de flotte en indicateurs d’émissions routières, de bruit et de qualité de l’air pour l’analyse de scénarios territoriaux."},
        "role": {"en": "My role covers the scientific and product roadmap, functional and system architecture, prioritisation, multidisciplinary coordination, partner demonstrations and the integration of models, APIs and geospatial services.", "fr": "Mon rôle couvre la feuille de route scientifique et produit, l’architecture fonctionnelle et système, la priorisation, la coordination pluridisciplinaire, les démonstrations partenaires et l’intégration des modèles, API et services géographiques."},
        "alt": {"en": "PLANET’AIR illustration connecting mobility data, emission models, atmospheric dispersion and territorial decision support.", "fr": "Illustration de PLANET’AIR reliant données de mobilité, modèles d’émissions, dispersion atmosphérique et aide à la décision territoriale."},
        "caption": {"en": "Conceptual illustration of the PLANET’AIR workflow.", "fr": "Illustration conceptuelle du workflow PLANET’AIR."},
        "flow": {"en": ["Mobility and fleet data", "Traffic and emission models", "Atmospheric dispersion", "Geospatial APIs and services", "Scenario comparison and decision support"], "fr": ["Données mobilité et flotte", "Trafic et émissions", "Dispersion atmosphérique", "API et services géographiques", "Comparaison de scénarios et aide à la décision"]},
    },
    {
        "id": "geco-air", "featured": True, "image": "img/projects/geco-air-project.avif", "logo": "img/geco-air-logo.avif", "width": 1600, "height": 900,
        "label": "Geco Air", "url": "https://gecoair.fr/", "video": "https://www.youtube-nocookie.com/embed/qd4ZlmutXas",
        "title": {"en": "Turning emission science into a deployed mobility service", "fr": "Transformer la science des émissions en service de mobilité déployé"},
        "summary": {"en": "Geco Air turns real mobility traces into understandable environmental indicators and feedback for everyday journeys.", "fr": "Geco Air transforme les traces réelles de mobilité en indicateurs environnementaux compréhensibles et en retours utiles pour les déplacements du quotidien."},
        "role": {"en": "My contribution connected scientific methodologies, emission models, backend services, integrations, product priorities and user experience.", "fr": "Ma contribution a relié méthodologies scientifiques, modèles d’émissions, services backend, intégrations, priorités produit et expérience utilisateur."},
        "alt": {"en": "Geco Air illustration showing multimodal trip tracking, environmental indicators and user feedback.", "fr": "Illustration de Geco Air montrant le suivi multimodal des déplacements, les indicateurs environnementaux et les retours proposés aux utilisateurs."},
        "caption": {"en": "Conceptual illustration of the Geco Air service.", "fr": "Illustration conceptuelle du service Geco Air."},
        "outcomes": {"en": ["70k+ users", "80M+ km analysed"], "fr": ["70 000+ utilisateurs", "80 M+ km analysés"]},
    },
    {
        "id": "wec", "featured": False, "image": "img/projects/wec-control-project.avif", "width": 1600, "height": 900,
        "label": {"en": "Wave energy control", "fr": "Commande de l’énergie houlomotrice"},
        "title": {"en": "Model predictive control for wave energy", "fr": "Commande prédictive pour l’énergie houlomotrice"},
        "summary": {"en": "A complete research workflow spanning modelling, predictive-control design, experimental validation and international WECCCOMP benchmarking.", "fr": "Une démarche complète associant modélisation, conception de commande prédictive, validation expérimentale et benchmark international WECCCOMP."},
        "alt": {"en": "Wave energy converter illustration combining modelling, predictive control, experimental validation and control-strategy benchmarking.", "fr": "Illustration d’un convertisseur d’énergie houlomotrice associant modélisation, commande prédictive, validation expérimentale et comparaison de stratégies de contrôle."},
        "caption": {"en": "Conceptual illustration; values shown in the visual are not reported results.", "fr": "Illustration conceptuelle ; les valeurs visibles ne constituent pas des résultats publiés."},
    },
    {
        "id": "phd", "featured": False, "image": "img/projects/phd-lunar-landing-project.avif", "width": 1600, "height": 900,
        "label": {"en": "PhD research", "fr": "Travaux de doctorat"},
        "title": {"en": "Bio-inspired perception for autonomous lunar landing", "fr": "Perception bio-inspirée pour l’atterrissage lunaire autonome"},
        "summary": {"en": "Research on optic flow, perception, state estimation and guidance-navigation-control that shaped my current systems-architecture approach.", "fr": "Travaux sur le flux optique, la perception, l’estimation d’état et le guidage-navigation-commande qui fondent mon approche actuelle d’architecture système."},
        "alt": {"en": "Illustration of Guillaume Sabiron’s PhD on bio-inspired perception, optic flow and guidance-navigation-control for autonomous lunar landing.", "fr": "Illustration du doctorat de Guillaume Sabiron sur la perception bio-inspirée, le flux optique et le guidage-navigation-commande pour l’atterrissage lunaire autonome."},
        "caption": {"en": "Conceptual illustration of the research workflow, not a depiction of a vehicle designed by Guillaume Sabiron.", "fr": "Illustration conceptuelle de la démarche de recherche, et non représentation d’un véhicule conçu intégralement par Guillaume Sabiron."},
    },
]

PUBLICATIONS = [
    {"id": "rtams-2025", "year": 2025, "type": {"en": "Book chapter", "fr": "Chapitre d’ouvrage"}, "title": "R-TAMS: An innovative decision support tool for real-time and prospective air quality and road traffic emissions monitoring", "authors": ["Guillaume Sabiron", "Suzanne Bussod"], "venue": "Springer LNITI", "pages": "874–885", "doi": "10.1007/978-3-031-82818-8_66", "url": "https://doi.org/10.1007/978-3-031-82818-8_66", "featured": True, "related_projects": ["planetair"], "synopsis": {"en": "A decision-support platform connecting traffic, emissions and air-quality modelling for territorial scenario analysis.", "fr": "Une plateforme d’aide à la décision reliant trafic, émissions et modélisation de la qualité de l’air pour l’analyse de scénarios territoriaux."}},
    {"id": "driving-behaviors-2024", "year": 2024, "type": {"en": "Conference publication", "fr": "Publication de conférence"}, "title": "Deep learning-based method for an assessment of road traffic pollutant estimation from predicted driving behaviors", "authors": ["Suzanne Bussod", "Guillaume Sabiron"], "venue": "International Conference on Machine Learning and Applications", "featured": True, "related_projects": ["planetair"], "synopsis": {"en": "A learning-based approach for estimating traffic pollutants from predicted driving behaviours.", "fr": "Une approche d’apprentissage pour estimer les polluants du trafic à partir de comportements de conduite prédits."}},
    {"id": "infrastructure-emissions-2023", "year": 2023, "type": {"en": "Journal paper", "fr": "Article de revue"}, "title": "A study on the impact of infrastructure on transport emissions based on real driving data", "authors": ["Guillaume Sabiron", "Mohamed Laraki"], "venue": "Transportation Research Procedia", "volume": "72", "pages": "2960–2967", "doi": "10.1016/j.trpro.2023.11.928", "url": "https://doi.org/10.1016/j.trpro.2023.11.928", "featured": True, "related_projects": ["geco-air"], "synopsis": {"en": "Real driving data used to assess how road infrastructure influences transport emissions and territorial decisions.", "fr": "Des données de conduite réelles pour évaluer l’influence des infrastructures sur les émissions de transport et les décisions territoriales."}},
    {"id": "weccomp-2023", "year": 2023, "type": {"en": "Journal article", "fr": "Article de revue"}, "title": "The wave energy converter control competition (WECCCOMP): Wave energy control algorithms compared in both simulation and tank testing", "authors": ["John V. Ringwood", "Nathan Tom", "Francesco Ferri", "Yi-Hsiang Yu", "Ryan G. Coe", "Kelley Ruehl", "Giorgio Bacelli", "Shuo Shi", "Ron J. Patton", "Paolino Tona", "Guillaume Sabiron", "Alexis Merigaud", "Bradley A. Ling", "Nicolas Faedo"], "venue": "Applied Ocean Research", "volume": "138", "pages": "103653", "doi": "10.1016/j.apor.2023.103653", "url": "https://doi.org/10.1016/j.apor.2023.103653", "featured": True, "related_projects": ["wec"], "synopsis": {"en": "An international benchmark comparing wave-energy control algorithms in simulation and wave-tank experiments.", "fr": "Un benchmark international comparant des algorithmes de commande houlomotrice en simulation et en bassin."}},
    {"id": "lunar-gnc-2015", "year": 2015, "type": {"en": "Journal article", "fr": "Article de revue"}, "title": "Suboptimal lunar landing GNC using nongimbaled optic-flow sensors", "authors": ["Guillaume Sabiron", "Thibaut Raharijaona", "Laurent Burlion", "Erwan Kervendal", "Eric Bornschlegl", "Franck Ruffier"], "venue": "IEEE Transactions on Aerospace and Electronic Systems", "volume": "51(4)", "pages": "2525–2545", "doi": "10.1109/TAES.2015.130573", "url": "https://doi.org/10.1109/TAES.2015.130573", "featured": True, "related_projects": ["phd"], "synopsis": {"en": "Optic-flow-based guidance, navigation and control for fuel-efficient autonomous lunar landing.", "fr": "Guidage, navigation et commande par flux optique pour un atterrissage lunaire autonome et économe en carburant."}},
    {"id": "lyon-capitale-2025", "year": 2025, "type": {"en": "Media", "fr": "Média"}, "title": "On risque de passer à côté de hotspots très localisés de pollution", "authors": ["Guillaume Sabiron"], "venue": "Lyon Capitale · 6 minutes chrono", "url": "https://www.lyoncapitale.fr/actualite/on-risque-de-passer-a-cote-de-hotspots-tres-localises-de-pollution-assure-guillaume-sabiron", "featured": True, "related_projects": ["planetair"], "synopsis": {"en": "A public discussion of localised pollution hotspots and high-resolution environmental modelling.", "fr": "Une contribution publique sur les hotspots de pollution localisés et la modélisation environnementale à haute résolution."}},
]


def featured_publications() -> list[dict]:
    return [item for item in PUBLICATIONS if item["featured"]]


def travel_countries() -> list[dict]:
    return [item for item in json.loads((ROOT / "data" / "travel_countries.json").read_text(encoding="utf-8"))["countries"] if item.get("display_on_map")]
