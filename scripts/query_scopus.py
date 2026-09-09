#!/usr/bin/env python3
"""
query_scopus.py

Scopus has no public search API available for this project, so this
script does not query it directly. Instead, it parses the BibTeX export
of the manual search done on the Scopus website using:

  TITLE(watermark OR watermarking)
  AND ALL(code OR "source code" OR program OR programming)
  AND ALL(LLM OR "large language model" OR "generative AI")
  AND PUBYEAR >= 2022

(saved as scripts/raw_data/scopus.bib), and extracts each entry's
metadata into screening_process/1_scopus.csv, using the same schema as
the other CSV files in the project: source, title, authors, year, venue,
doi, url, abstract.

Note on authors: names are kept exactly as exported by Scopus's BibTeX
("Li, Boquan and Fu, Zirui and ...") -- only the "and" separator is
normalized to "; "; given names are not abbreviated or reordered.

Usage:
  pip install bibtexparser
  python3 query_scopus.py
  python3 query_scopus.py --input raw_data/scopus.bib --out screening_process
"""

import argparse
import csv
import html
import os
import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_INPUT_FILE = os.path.join(SCRIPT_DIR, "raw_data", "scopus.bib")
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "screening_process")

YEAR_FROM = 2022

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]


def clean_text(value):
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def format_authors(raw):
    """Only normalizes the BibTeX 'and' separator to '; '; names themselves
    (given names, order, spelling) are left exactly as exported."""
    if not raw:
        return ""
    parts = [p.strip() for p in re.split(r"\s+and\s+", raw.strip()) if p.strip()]
    return "; ".join(clean_text(p) for p in parts)


def entry_to_row(entry):
    return {
        "source": "Scopus",
        "title": clean_text(entry.get("title", "")),
        "authors": format_authors(entry.get("author", "")),
        "year": clean_text(entry.get("year", "")),
        "venue": clean_text(entry.get("journal", "")),
        "doi": clean_text(entry.get("doi", "")),
        "url": clean_text(entry.get("url", "")),
        "abstract": clean_text(entry.get("abstract", "")),
    }


def parse_bib(input_file):
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    with open(input_file, encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)

    print(f"[Scopus] parsing {len(db.entries)} entries from {input_file}")

    rows = []
    for entry in db.entries:
        year_str = entry.get("year", "").strip()
        if year_str.isdigit() and int(year_str) < YEAR_FROM:
            print(f"  skipping '{entry.get('title', '')[:60]}' (year {year_str} before {YEAR_FROM})")
            continue
        rows.append(entry_to_row(entry))
    return rows


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
        default=DEFAULT_INPUT_FILE,
        help=f"BibTeX file exported from Scopus (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output folder (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    rows = parse_bib(args.input)
    write_csv(os.path.join(args.out, "1_scopus.csv"), rows)


if __name__ == "__main__":
    main()
