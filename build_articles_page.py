"""
Turn arxiv_tda_raw.jsonl into a Quarto listing page for the TDA website.

Writes:
    articles/papers.yml   - one entry per paper (title, link, authors, date, tags)
    articles.qmd          - the page: searchable, sortable, filterable by tag

Tags for now = the arXiv search queries that matched each paper
(later you can swap in your own classifier's labels).

Usage (run from the root of the website repo, next to _quarto.yml):
    python build_articles_page.py
Reads data/arxiv_tda_raw.jsonl by default; use --src to point elsewhere.
"""

import argparse
import json
import os

# Search query name -> tag shown on the site
TAG_NAMES = {
    # Core TDA
    "tda": "TDA",
    "persistent_homology": "Persistent homology",
    "persistence_diagram": "Persistence diagrams",
    "persistence_module": "Persistence modules",
    "mapper": "Mapper",
    "zigzag": "Zigzag persistence",
    "multiparameter": "Multiparameter persistence",
    "vietoris_rips": "Vietoris-Rips / Cech",
    "euler_characteristic_curve": "Euler characteristic",
    "persistence_landscape": "Vectorisation",
    # Applications
    "topological_ml": "Topological ML",
    "topological_loss": "Topological loss",
    "ph_images": "App: images",
    "ph_biology": "App: biology & medicine",
    "ph_time_series": "App: time series",
    "ph_materials": "App: materials & chemistry",
    "ph_networks": "App: graphs & networks",
    # Maths background
    "spectral_sequence_persistence": "Spectral sequences",
    "discrete_morse": "Discrete Morse theory",
    "sheaf_tda": "Sheaves",
    "computational_topology": "Computational topology",
    "stability_theorem": "Stability",
    "interleaving_distance": "Interleaving / bottleneck distance",
    "math_AT_applied": "Algebraic topology (math.AT)",
}

PAGE = """---
title: "Article database"
subtitle: "{n} arXiv papers on topological data analysis, its applications and its maths background. Click a tag to filter, or search by title or author."
listing:
  id: papers
  contents: articles/papers.yml
  type: table
  fields: [date, title, author, categories]
  field-display-names:
    date: "Published"
    title: "Title"
    author: "Authors"
    categories: "Tags"
  sort: "date desc"
  sort-ui: [date, title]
  filter-ui: [title, author]
  categories: true
  page-size: 50
  date-format: "YYYY-MM-DD"
---

Raw scrape from the arXiv API, last updated {updated}. Tags come from the search
queries that matched each paper, so a paper can carry several, and some will be
noisy until the papers are cleaned and classified.
"""


def short_authors(authors, n=3):
    if not authors:
        return ""
    return ", ".join(authors[:n]) + (" et al." if len(authors) > n else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join("data", "arxiv_tda_raw.jsonl"))
    ap.add_argument("--site-dir", default=".", help="root of the Quarto site")
    args = ap.parse_args()

    items, latest = [], ""
    with open(args.src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = json.loads(line)
            date = (p.get("published") or "")[:10]
            latest = max(latest, (p.get("updated") or "")[:10])
            items.append({
                "title": p["title"],
                "path": p["abs_url"],
                "author": short_authors(p.get("authors", [])),
                "date": date,
                "categories": [TAG_NAMES.get(q, q) for q in p.get("matched_queries", [])],
            })

    out_dir = os.path.join(args.site_dir, "articles")
    os.makedirs(out_dir, exist_ok=True)
    # JSON is valid YAML, so no PyYAML needed and quoting is always safe.
    with open(os.path.join(out_dir, "papers.yml"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)

    with open(os.path.join(args.site_dir, "articles.qmd"), "w", encoding="utf-8") as f:
        f.write(PAGE.format(n=f"{len(items):,}", updated=latest))

    print(f"Wrote {len(items)} papers to articles/papers.yml and the page to articles.qmd")


if __name__ == "__main__":
    main()