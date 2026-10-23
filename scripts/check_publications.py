#!/usr/bin/env python3
"""Find newly published papers and add them to the Publications page.

Queries Crossref and OpenAlex for papers by the author, skips preprints and
anything listed under `known` in _data/publications_check.yml or already on
the page, and inserts the rest at the top of _publications/index.html in the
page's format. Added papers are also appended to `known`, and a Markdown
summary for the pull request goes to --summary.

Usage: check_publications.py [--summary out.md] [--dry-run] [--seed]
  --seed  record every paper found as known without touching the page
"""
import argparse
import datetime
import difflib
import html
import json
import re
import sys
import urllib.parse
import urllib.request

import yaml

DATA = "_data/publications_check.yml"
PAGE = "_publications/index.html"
UA = {"User-Agent": "machiry.github.io publications checker"}
SKIP_TYPES = {"preprint", "posted-content", "dataset", "other", "peer-review", "dissertation"}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def clean_title(title):
    """Drops LaTeX and markup, e.g. "$ZTD_{\\text{JAVA}}$" -> "ZTDJAVA"."""
    title = html.unescape(re.sub(r"<[^>]+>", "", title))
    title = re.sub(r"\\[a-zA-Z]+|[${}_^]", "", title)
    return re.sub(r"\s+", " ", title).strip()


def norm(title):
    title = re.sub(r"\s*\([^)]*\)\s*$", "", clean_title(title))  # e.g. "(Experience Paper)"
    return re.sub(r"[^a-z0-9]", "", title.lower())


def same_title(a, b):
    a, b = norm(a), norm(b)
    if min(len(a), len(b)) >= 30 and (a.startswith(b) or b.startswith(a)):
        return True
    return a == b or difflib.SequenceMatcher(None, a, b).ratio() >= 0.9


def initials(given, family):
    parts = re.split(r"[\s.-]+", given or "")
    return " ".join(p[0].upper() + "." for p in parts if p) + " " + family if parts != [""] else family


def crossref(cfg, since):
    url = ("https://api.crossref.org/works?rows=200&query.author=" +
           urllib.parse.quote(cfg["author_display"]) + f"&filter=from-pub-date:{since}" +
           "&select=DOI,title,author,container-title,issued,type,issue")
    works = []
    for w in get_json(url)["message"]["items"]:
        authors = w.get("author", [])
        if not w.get("title") or not any(a.get("family") == cfg["author_family"] for a in authors):
            continue
        works.append({
            "doi": w["DOI"].lower(),
            "title": clean_title(w["title"][0]),
            "authors": [(a.get("given", ""), a.get("family", "")) for a in authors],
            "venue": (w.get("container-title") or [""])[0],
            "issue": w.get("issue", ""),
            "year": w["issued"]["date-parts"][0][0],
            "type": w["type"],
        })
    return works


def openalex(cfg, since):
    url = (f"https://api.openalex.org/works?per-page=200&filter=author.id:{cfg['openalex_author']},"
           f"from_publication_date:{since}-01-01"
           "&select=doi,title,authorships,primary_location,publication_year,type")
    works = []
    for w in get_json(url)["results"]:
        if not w.get("title"):
            continue
        names = [a["author"]["display_name"].rsplit(" ", 1) for a in w["authorships"]]
        source = (w.get("primary_location") or {}).get("source") or {}
        works.append({
            "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower(),
            "title": clean_title(w["title"]),
            "authors": [(n[0], n[1]) if len(n) == 2 else ("", n[0]) for n in names],
            "venue": source.get("display_name") or "",
            "issue": "",
            "year": w["publication_year"],
            "type": w["type"],
        })
    return works


def label(cfg, work):
    if work["venue"].startswith("Proceedings of the ACM on") and work["issue"]:
        return work["issue"]
    for venue in cfg["venues"]:
        if venue["match"].lower() in work["venue"].lower():
            return venue["label"]
    return None


def entry(cfg, work, venue_label):
    authors = []
    for given, family in work["authors"]:
        if family == cfg["author_family"]:
            authors.append(f"<b> {cfg['author_display']} </b>")
        else:
            authors.append(initials(given, family))
    link = f'\t\t[<a href="https://doi.org/{work["doi"]}">doi</a>]\n' if work["doi"] else ""
    return (
        "\t<p>\n\n"
        f"\t\t<strong>{html.escape(work['title'], quote=False)}</strong><br>\n"
        f"\t\t{', '.join(authors)}.<br>\n"
        f"\t\t<b> {venue_label or 'VENUE?'} {work['year']} </b> : {html.escape(work['venue'], quote=False)}. <br>\n"
        f"{link}"
        "\t</p>\n\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed", action="store_true")
    args = ap.parse_args()

    cfg_src = open(DATA, encoding="utf-8").read()
    cfg = yaml.safe_load(cfg_src)
    known = cfg.get("known") or []
    page = open(PAGE, encoding="utf-8").read()
    on_page = re.findall(r"<strong>(.*?)</strong>", page, re.S)
    since = datetime.date.today().year - (100 if args.seed else 1)

    works = []
    for source in (crossref, openalex):
        try:
            found = source(cfg, since)
        except Exception as e:
            print(f"::warning::{source.__name__} query failed: {e}")
            continue
        for w in found:
            if w["type"] in SKIP_TYPES:
                continue
            if any((w["doi"] and w["doi"] == o["doi"]) or same_title(w["title"], o["title"]) for o in works):
                continue  # Crossref comes first and has the better metadata
            works.append(w)

    new = []
    for w in works:
        if any((w["doi"] and w["doi"] == (k.get("doi") or "").lower()) or same_title(w["title"], k["title"])
               for k in known):
            continue
        if not args.seed and any(same_title(w["title"], t) for t in on_page):
            continue
        new.append(w)
    new.sort(key=lambda w: w["year"], reverse=True)

    lines = []
    if new and not args.seed:
        first = page.index("<p>", page.index('<div class="cv">'))
        block = "".join(entry(cfg, w, label(cfg, w)) for w in new)
        page = page[:first] + block.lstrip("\t") + "\t" + page[first:]
        lines.append("New papers added to the top of the Publications page:\n")
        lines.append("| Title | Venue | Year | Label |\n|---|---|---|---|")
        for w in new:
            venue_label = label(cfg, w)
            lines.append(f"| {w['title']} | {w['venue']} | {w['year']} | "
                         f"{venue_label or '**unknown: edit `VENUE?`**'} |")
        lines.append("\nBefore merging: check author names and the venue line, add the PDF link, "
                     "and consider a Recent News item on the home page. To leave a paper off the "
                     "page, delete its entry here but keep it under `known` in "
                     "`_data/publications_check.yml`.")

    if new:
        cfg_src = cfg_src.rstrip("\n") + "\n" + "".join(
            f"  - {{doi: {json.dumps(w['doi'])}, title: {json.dumps(w['title'])}}}\n" for w in new)
    if new and not args.dry_run:
        open(DATA, "w", encoding="utf-8").write(cfg_src)
        if not args.seed:
            open(PAGE, "w", encoding="utf-8").write(page)

    summary = "\n".join(lines) or ("Recorded %d papers as known." % len(new) if args.seed
                                   else "No new papers found.")
    print(summary)
    if args.summary:
        open(args.summary, "w", encoding="utf-8").write(summary + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
