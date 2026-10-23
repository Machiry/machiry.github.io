#!/usr/bin/env python3
"""Find new program committee memberships and add them to _data/service.yml.

Searches each venue's committee pages (the `check` URLs in the data file) for
recent years, and reads the conf.researchr.org profile. New years are written
into the `years:` lines of the data file, and a Markdown summary for the pull
request goes to --summary.

Usage: check_service.py [--data _data/service.yml] [--summary out.md] [--dry-run]
"""
import argparse
import datetime
import html
import re
import sys
import urllib.parse
import urllib.request

import yaml

NAME = "Machiry"  # some pages list names last-first
UA = {"User-Agent": "Mozilla/5.0 (machiry.github.io service-page checker)"}
LINK = re.compile(r'href="([^"#]+)"[^>]*>(.*?)</a>', re.I | re.S)
COMMITTEE = re.compile(r"committee|organi[sz]|leadership|people|prog(ram)?-?c\b", re.I)
ASSET = re.compile(r"\.(ico|png|jpe?g|gif|svg|css|js|pdf|zip)(\?|$)", re.I)
HEADING = re.compile(r"<(h[1-6]|strong|b|dt|th)\b[^>]*>(.*?)</\1>", re.I | re.S)


def fetch(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", "ignore")
    except Exception:
        return None


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def role_hint(page):
    """The last heading before the name, e.g. "PC Members" or "Associate Chairs"."""
    i = page.find("Machiry")
    heads = [text(h[1]) for h in HEADING.findall(page[:i])]
    heads = [h for h in heads if 0 < len(h) < 60]
    return heads[-1] if heads else "unknown"


def search(url):
    """Returns (status, page URL, role) where status is hit, miss or unreachable."""
    page = fetch(url)
    if page is None:
        return "unreachable", url, None
    if NAME in text(page):
        return "hit", url, role_hint(page)
    host = urllib.parse.urlparse(url).netloc
    seen = set()
    for href, label in LINK.findall(page):
        link = urllib.parse.urljoin(url, html.unescape(href))
        if link in seen or urllib.parse.urlparse(link).netloc != host or ASSET.search(link):
            continue
        if not COMMITTEE.search(href + " " + text(label)):
            continue
        seen.add(link)
        sub = fetch(link)
        if sub and NAME in text(sub):
            return "hit", link, role_hint(sub)
    return "miss", url, None


def researchr_roles(url):
    """Returns [(year, conference, role)] for committee and chair roles."""
    page = fetch(url)
    if page is None:
        print(f"::warning::could not fetch researchr profile {url}")
        return []
    page = re.sub(r"(?s)<(script|style).*?</\1>", "", page)
    lines = [l.strip() for l in html.unescape(re.sub(r"<[^>]+>", "\n", page)).split("\n") if l.strip()]
    roles, year, conf = [], None, None
    for line in lines[lines.index("Contributions") + 1:] if "Contributions" in lines else []:
        if re.fullmatch(r"(19|20)\d\d", line):
            year = int(line)
        elif re.search(r"Committee|Chair", line) and not line.startswith(("Author", "Session Chair")):
            roles.append((year, conf, line))
        elif not line.startswith(("Author", "Session Chair")) and len(line) < 30:
            conf = line
    return roles


def add_year(src, name, year):
    """Inserts `year` into the one-line `years:` list of entry `name`."""
    pattern = re.compile(
        r"(- name: " + re.escape(name) + r"\n(?:[ \t]+\S.*\n)*?[ \t]+years: \[)([^\]]*)(\])")
    m = pattern.search(src)
    if not m:
        raise ValueError(f"no one-line years list for {name!r}")
    years = sorted({int(y) for y in re.findall(r"\d{4}", m.group(2))} | {year}, reverse=True)
    return src[:m.start(2)] + ", ".join(map(str, years)) + src[m.end(2):]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="_data/service.yml")
    ap.add_argument("--summary")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = open(args.data, encoding="utf-8").read()
    data = yaml.safe_load(src)
    this_year = datetime.date.today().year
    years = range(this_year - 1, this_year + 2)

    known = {}
    for entry in data["program_committees"] + data.get("chairs", []):
        key = entry.get("venue", entry["name"])
        known.setdefault(key, set()).update(entry["years"])

    found = []  # (entry name, year, url, role)
    for venue in data["program_committees"]:
        reachable = False
        for year in years:
            if year in known[venue["name"]]:
                continue
            for template in venue.get("check", []):
                url = template.replace("{yyyy}", str(year)).replace("{yy}", f"{year % 100:02d}")
                status, where, role = search(url)
                print(f"{status:11} {venue['name']} {year}: {where}")
                reachable |= status != "unreachable"
                if status == "hit":
                    found.append((venue["name"], year, where, role))
                    break
        if venue.get("check") and not reachable and any(y not in known[venue["name"]] for y in years):
            print(f"::warning::no committee page reachable for {venue['name']}; check its URLs")

    unmapped = []
    entries = data["program_committees"] + data.get("chairs", [])
    for year, conf, role in researchr_roles(data["researchr_profile"]):
        match = [e for e in entries if e.get("researchr") and e["researchr"] in role]
        if not match:
            unmapped.append((year, conf, role))
        elif year not in match[0]["years"]:
            found.append((match[0]["name"], year, data["researchr_profile"], role))

    for name, year, _, _ in found:
        src = add_year(src, name, year)
    if found and not args.dry_run:
        open(args.data, "w", encoding="utf-8").write(src)

    lines = []
    if found:
        lines.append("Found new committee memberships:\n")
        lines.append("| Venue | Year | Nearest heading on page | Source |\n|---|---|---|---|")
        for name, year, url, role in found:
            lines.append(f"| {name} | {year} | {role} | [link]({url}) |")
        lines.append("\nThe year was added to the program committee list. If the role is a "
                     "chair, move it to `chairs` in `_data/service.yml` before merging.")
    if unmapped:
        lines.append("\nRoles on researchr with no matching entry (add them by hand if wanted):\n")
        lines += [f"- {year} {conf}: {role}" for year, conf, role in unmapped]
    summary = "\n".join(lines) or "No new committee memberships found."
    print("\n" + summary)
    if args.summary:
        open(args.summary, "w", encoding="utf-8").write(summary + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
