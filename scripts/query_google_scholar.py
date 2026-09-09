#!/usr/bin/env python3
"""
query_google_scholar.py

Google Scholar has no official API and blocks automated queries (CAPTCHA)
very aggressively, so this script does not query Google Scholar itself.
Instead, it parses the HTML of Google Scholar result pages that were
saved manually (Ctrl/Cmd+S "Webpage, HTML only") while browsing the
search for:

  (intitle:watermark OR intitle:watermarking)
  AND (code OR "source code" OR program OR programming)
  AND (LLM OR "large language model" OR "generative AI")

restricted to 2022-2026, and extracts each result's metadata into
screening_process/1_google_scholar.csv, using the same schema as the
other CSV files in the project: source, title, authors, year, venue, doi,
url, abstract.

Usage:
  python3 query_google_scholar.py
  python3 query_google_scholar.py --input raw_data/google_scholar --out screening_process
"""

import argparse
import csv
import glob
import os
import re

from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_INPUT_DIR = os.path.join(SCRIPT_DIR, "raw_data", "google_scholar")
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "screening_process")

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]

TAG_PREFIX_RE = re.compile(r"^\[(PDF|HTML|CITATION|BOOK)\]\s*", re.IGNORECASE)


def clean_title(title):
    while True:
        new_title = TAG_PREFIX_RE.sub("", title)
        if new_title == title:
            return new_title
        title = new_title


def clean_text(el):
    """Extract text from an element without inserting extra spaces at tag
    boundaries. Scholar wraps matched keywords in <b> tags right up against
    adjacent punctuation/words (e.g. 'code</b>?'), so a separator-based
    get_text() would introduce spaces that aren't in the source. Also
    normalizes the non-breaking spaces (\\xa0) Scholar uses around the
    ' - ' separators in the byline, which would otherwise stop those
    separators from being matched literally."""
    text = el.get_text().replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_gs_a(text):
    """Parse the 'div.gs_a' byline, e.g. 'A Author, B Author - Venue, 2024
    - example.com' into (authors, year, venue)."""
    parts = [p.strip() for p in text.split(" - ")]
    authors = parts[0] if parts else ""
    year_match = re.search(r"\b(19|20)\d{2}\b", text)
    year = year_match.group(0) if year_match else ""
    venue = ""
    if len(parts) > 1:
        venue = re.sub(r",?\s*\b(19|20)\d{2}\b.*$", "", parts[1]).strip()
    return authors, year, venue


def parse_file(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for block in soup.select("div.gs_ri"):
        title_el = block.select_one("h3.gs_rt")
        if not title_el:
            continue
        link_el = title_el.select_one("a")
        title = clean_text(link_el) if link_el else clean_text(title_el)
        title = clean_title(title)
        url = link_el["href"] if link_el and link_el.has_attr("href") else ""

        gs_a_el = block.select_one("div.gs_a")
        authors, year, venue = parse_gs_a(clean_text(gs_a_el)) if gs_a_el else ("", "", "")

        abstract_el = block.select_one("div.gs_rs")
        abstract = clean_text(abstract_el) if abstract_el else ""

        rows.append({
            "source": "Google Scholar",
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "doi": "",
            "url": url,
            "abstract": abstract,
        })
    return rows


def parse_saved_pages(input_dir):
    files = sorted(glob.glob(os.path.join(input_dir, "*.html")))
    if not files:
        raise SystemExit(f"No .html files found in {input_dir}")

    print(f"[Google Scholar] parsing {len(files)} saved pages from {input_dir}")
    all_rows = []
    for path in files:
        rows = parse_file(path)
        print(f"  {os.path.basename(path)}: {len(rows)} results")
        all_rows.extend(rows)

    seen = set()
    deduped = []
    for r in all_rows:
        key = r["title"].strip().lower()
        if key and key not in seen:
            seen.add(key)
            deduped.append(r)

    print(f"[Google Scholar] {len(all_rows)} rows parsed, {len(deduped)} unique by title")
    return deduped


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDNAMES})
    print(f"  -> {len(rows)} records saved to {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_DIR,
        help=f"Folder with saved Google Scholar HTML pages (default: {DEFAULT_INPUT_DIR})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output folder (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    rows = parse_saved_pages(args.input)
    write_csv(os.path.join(args.out, "1_google_scholar.csv"), rows)


if __name__ == "__main__":
    main()
