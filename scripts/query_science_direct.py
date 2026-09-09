#!/usr/bin/env python3
"""
query_science_direct.py

ScienceDirect has no public search API, so this script does not query it
directly. Instead, it parses the BibTeX export of the manual search done
on the ScienceDirect website using:

  Find articles with these terms:
    (code OR "source code" OR program OR programming)
    AND (LLM OR "large language model" OR "generative AI")

  Title:
    watermark OR watermarking

(publication period 2022-2026, applied via ScienceDirect's own website
filters and saved as scripts/raw_data/science_direct.bib), and extracts
each entry's metadata into screening_process/1_science_direct.csv, using
the same schema as the other CSV files in the project: source, title,
authors, year, venue, doi, url, abstract.

Usage:
  pip install bibtexparser
  python3 query_science_direct.py
  python3 query_science_direct.py --input raw_data/science_direct.bib --out screening_process
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

DEFAULT_INPUT_FILE = os.path.join(SCRIPT_DIR, "raw_data", "science_direct.bib")
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "screening_process")

YEAR_FROM = 2022
YEAR_TO = 2027

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]

DOI_URL_PREFIX_RE = re.compile(r"^https?://(dx\.)?doi\.org/", re.IGNORECASE)


def clean_text(value):
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def clean_doi(raw):
    """ScienceDirect exports the doi field as a full https://doi.org/...
    URL rather than a bare identifier; strip that prefix to match the
    project's schema (bare DOI in 'doi', full link in 'url')."""
    doi = clean_text(raw)
    return DOI_URL_PREFIX_RE.sub("", doi)


def format_authors(raw):
    if not raw:
        return ""
    names = []
    for part in re.split(r"\s+and\s+", raw.strip()):
        part = part.strip()
        if not part:
            continue
        if "," in part:
            last, _, first = part.partition(",")
            names.append(f"{first.strip()} {last.strip()}")
        else:
            names.append(part)
    return "; ".join(clean_text(n) for n in names)


def entry_to_row(entry):
    venue = entry.get("journal") or entry.get("booktitle") or ""
    return {
        "source": "ScienceDirect",
        "title": clean_text(entry.get("title", "")),
        "authors": format_authors(entry.get("author", "")),
        "year": clean_text(entry.get("year", "")),
        "venue": clean_text(venue),
        "doi": clean_doi(entry.get("doi", "")),
        "url": clean_text(entry.get("url", "")),
        "abstract": clean_text(entry.get("abstract", "")),
    }


def parse_bib(input_file):
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    with open(input_file, encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)

    print(f"[ScienceDirect] parsing {len(db.entries)} entries from {input_file}")

    rows = []
    for entry in db.entries:
        year_str = entry.get("year", "").strip()
        if year_str.isdigit() and not (YEAR_FROM <= int(year_str) <= YEAR_TO):
            print(f"  skipping '{entry.get('title', '')[:60]}' (year {year_str} out of range)")
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
        help=f"BibTeX file exported from ScienceDirect (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output folder (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    rows = parse_bib(args.input)
    write_csv(os.path.join(args.out, "1_science_direct.csv"), rows)


if __name__ == "__main__":
    main()
