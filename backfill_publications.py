#!/usr/bin/env python3
"""
One-off backfill: rewrites existing _publications/*.md files in the clean format
(description / authors / DOI / figure placeholder), pulling authors and abstracts
from Crossref by DOI when possible. Falls back to a hand-written description per
permalink when Crossref doesn't expose an abstract.
"""

import html
import re
import sys
import time
from pathlib import Path

import requests
import yaml

PUBLICATIONS_DIR = Path("_publications")
IMAGES_DIR = "images/papers"

# Hand-written plain-language descriptions used when Crossref doesn't provide
# an abstract (Nature, AGU, Wiley typically don't expose one via Crossref).
FALLBACK_DESCRIPTIONS = {
    # 2024 published
    "2024-Climate-change-will-reduce-North-American-inland-w":
        "Projects how warming will shrink inland wetland area across North America and shift the seasonal timing of wetland flooding.",
    "2024-Disentangling-the-hydrological-and-hydraulic-contr":
        "Separates the hydrological and hydraulic contributions to streamflow variability in E3SM v2, using the Pantanal wetland as a case study.",
    "2024-Quantifying-the-impacts-of-land-cover-change-on-th":
        "Quantifies how land-cover change in the Lower Mississippi River Basin altered the hydrologic response to Hurricane Ida.",
    "2024-Simulation-of-Compound-Flooding-Using-RiverOcean-T":
        "Simulates compound coastal flooding with a two-way coupled river-ocean configuration of E3SM on a variable-resolution mesh.",
    "2024-wmpy-power-A-Python-package-for-process-based-regi":
        "Introduces wmpy-power, a Python package for process-based regional hydropower simulation that supports reproducible reservoir and generation modeling at scale.",
    # 2025 published
    "2025-Impacts-of-irrigation-expansion-on-moist-heat-stre":
        "Uses the IRRMIP multi-model intercomparison to show how expanding irrigation modifies regional moist-heat stress and human heat exposure.",
    "2025-Evaluation-of-CMIP6-streamflow-in-the-Arctic":
        "Evaluates how well CMIP6-generation Earth system models reproduce observed streamflow across Arctic river basins.",
    "2025-Evaluation-of-Flow-Routing-on-the-Unstructured-Vor":
        "Tests river flow routing schemes on unstructured Voronoi meshes used in Earth system modeling and compares accuracy and performance against structured-grid baselines.",
    "2025-Improving-the-prediction-of-daily-reservoir-releas":
        "Trains a conditioned LSTM to predict daily reservoir releases across the contiguous United States, improving on operational baselines.",
    "2026-The-Energy-Exascale-Earth-System-Model-Version-3-2":
        "Overview paper describing the coupled configuration and evaluation of version 3 of the DOE Energy Exascale Earth System Model (E3SM).",
    # Preprints
    "2024-Disentangling-Atmospheric-Hydrological-and-Couplin":
        "Examines how atmospheric forcing, hydrologic processes, and model coupling each contribute to uncertainty in compound-flood predictions from a coupled Earth system model.",
    "2025-A-new-Dataset-for-Belowground-Urban-Stormwater-Net":
        "Releases a continental-scale dataset describing belowground urban stormwater drainage networks across the United States, enabling broader urban hydrology modeling.",
    "2025-Muted-Global-Changes-Despite-Large-Regional-Respon":
        "Projects future wetland change globally, finding that strong opposing regional shifts in inundated and saturated wetland extent largely cancel out at the global scale.",
    "2025-The-past-and-future-changes-of-river-suspended-sed":
        "Quantifies historical trends and future projections of river suspended sediment loads across the U.S. Mid-Atlantic.",
    "2026-Can-We-Trust-LLMs-for-Complex-Earth-System-Model-A":
        "Benchmarks large language models on Earth system model analysis tasks and documents silent-failure modes where outputs look plausible but are wrong.",
}

# Files we want to rewrite (the 15 ORCID-generated 2024+ entries)
TARGET_PERMALINKS = set(FALLBACK_DESCRIPTIONS.keys())


def fetch_crossref(doi: str) -> dict:
    if not doi:
        return {}
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{doi}",
            timeout=15,
            headers={"User-Agent": "hydrotian-jekyll-backfill/1.0 (mailto:hydro.tian@gmail.com)"},
        )
        if r.status_code != 200:
            return {}
        return r.json().get("message", {}) or {}
    except (requests.RequestException, ValueError):
        return {}


def clean_jats(s: str) -> str:
    """Strip JATS/HTML tags from a Crossref abstract."""
    if not s:
        return ""
    s = re.sub(r"<jats:title[^>]*>.*?</jats:title>", "", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", "", s)
    # Decode entities twice: Crossref sometimes double-encodes (&amp;#8217; -> &#8217; -> ’)
    s = html.unescape(html.unescape(s))
    s = re.sub(r"\s+", " ", s).strip()
    if s.lower().startswith("abstract."):
        s = s[len("abstract."):].strip()
    elif s.lower().startswith("abstract"):
        s = s[len("abstract"):].lstrip(" .:").strip()
    return s


def first_sentences(text: str, max_chars: int = 350) -> str:
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for p in parts:
        if not out:
            out = p
        elif len(out) + 1 + len(p) <= max_chars:
            out = f"{out} {p}"
        else:
            break
    return out


def authors_from_crossref(msg: dict) -> str:
    arr = msg.get("author") or []
    names = []
    for a in arr:
        family = a.get("family", "").strip()
        given = a.get("given", "").strip()
        if not family:
            continue
        initials = " ".join(f"{p[0]}." for p in given.split() if p)
        names.append(f"{family}, {initials}".strip().rstrip(","))
    if len(names) <= 5:
        return ", ".join(names)
    return ", ".join(names[:5]) + ", et al."


def parse_frontmatter(text: str) -> tuple:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, flags=re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def rewrite_file(path: Path):
    raw = path.read_text(encoding="utf-8")
    fm, _body = parse_frontmatter(raw)
    if not fm:
        print(f"skip (no frontmatter): {path.name}")
        return

    permalink_stem = path.stem
    if permalink_stem not in TARGET_PERMALINKS:
        return

    paper_url = fm.get("paperurl", "") or ""
    doi_match = re.search(r"10\.\d{4,9}/[^\s]+", paper_url)
    doi = doi_match.group(0).rstrip(" .)") if doi_match else ""

    cr = fetch_crossref(doi)
    abstract = clean_jats(cr.get("abstract", ""))
    description = first_sentences(abstract) if abstract else ""
    if not description:
        description = FALLBACK_DESCRIPTIONS.get(permalink_stem, fm.get("excerpt", ""))

    authors = authors_from_crossref(cr) or fm.get("authors", "") or ""

    # Venue: prefer existing, then Crossref container-title, then a DOI-prefix heuristic
    venue = fm.get("venue") or ""
    if not venue:
        ct = cr.get("container-title") or []
        if ct:
            venue = ct[0]
    if not venue and doi:
        d = doi.lower()
        if d.startswith("10.5194/egusphere"):
            venue = "EGUsphere (preprint)"
        elif d.startswith("10.5194/"):
            venue = "Copernicus (preprint)"
        elif d.startswith("10.21203/"):
            venue = "Research Square (preprint)"
        elif d.startswith("10.22541/essoar") or d.startswith("10.1002/essoar"):
            venue = "ESS Open Archive (preprint)"
        elif "arxiv" in d:
            venue = "arXiv"

    pubtype = fm.get("pubtype")
    if not pubtype:
        # Heuristic: Copernicus EGUsphere/HESSD/etc preprints we already know are preprints
        pubtype = "preprint" if "egusphere" in paper_url.lower() or "preprint" in (fm.get("venue", "")).lower() else "journal-article"

    new_fm = {
        "title": fm.get("title", ""),
        "collection": "publications",
        "permalink": fm.get("permalink", f"/publication/{permalink_stem}"),
        "excerpt": description,
        "date": fm.get("date", ""),
        "venue": venue,
        "paperurl": paper_url,
        "authors": authors,
        "pubtype": pubtype,
        "comments": True,
    }

    body_lines = [description, ""]
    if authors:
        body_lines += [f"**Authors:** {authors}", ""]
    if paper_url:
        label = doi if doi else paper_url
        body_lines += [f"**DOI:** [{label}]({paper_url})", ""]
    image_filename = f"{permalink_stem}.png"
    body_lines += [
        f"<!-- Drop a figure into /{IMAGES_DIR}/{image_filename} and uncomment: -->",
        f"<!-- ![figure](/{IMAGES_DIR}/{image_filename}) -->",
        "",
    ]

    new_text = (
        "---\n"
        + yaml.dump(new_fm, default_flow_style=False, allow_unicode=True, sort_keys=True)
        + "---\n"
        + "\n".join(body_lines)
    )
    path.write_text(new_text, encoding="utf-8")
    src = "crossref" if abstract else "fallback"
    print(f"rewrote {path.name} (description: {src})")


def main():
    targets = sorted(PUBLICATIONS_DIR.glob("*.md"))
    for p in targets:
        rewrite_file(p)
        time.sleep(0.2)  # be polite to Crossref


if __name__ == "__main__":
    main()
