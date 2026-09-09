#!/usr/bin/env python3
"""
query_ieee_xplore.py

IEEE Xplore has no public search API, so this script does not query it
directly. Instead, it parses the CSV export of the manual search done on
the IEEE Xplore website using:

  ("Document Title":watermark OR "Document Title":watermarking)
  AND ("Full Text & Metadata":code OR "Full Text & Metadata":"source code"
       OR "Full Text & Metadata":program OR "Full Text & Metadata":programming)
  AND ("Full Text & Metadata":LLM OR "Full Text & Metadata":"large language model"
       OR "Full Text & Metadata":"generative AI")

(publication period 2022-2026, applied via IEEE Xplore's own website
filters and saved as scripts/raw_data/ieee_xplore.csv), and extracts each
row's metadata into screening_process/1_ieee_xplore.csv, using the same
schema as the other CSV files in the project: source, title, authors,
year, venue, doi, url, abstract.

Usage:
  python3 query_ieee_xplore.py
  python3 query_ieee_xplore.py --input raw_data/ieee_xplore.csv --out screening_process
"""

import argparse
import csv
import html
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_INPUT_FILE = os.path.join(SCRIPT_DIR, "raw_data", "ieee_xplore.csv")
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "screening_process")

YEAR_FROM = 2022
YEAR_TO = 2026

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]

ARNUMBER_RE = re.compile(r"arnumber=(\d+)")


def clean_text(value):
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def document_url(pdf_link):
    """IEEE Xplore's export gives a 'stamp.jsp?arnumber=...' PDF link, not
    the article page; rebuild the canonical /document/<arnumber> URL from
    it, matching the format used for the other IEEE records in the
    project."""
    match = ARNUMBER_RE.search(pdf_link or "")
    if not match:
        return clean_text(pdf_link)
    return f"https://ieeexplore.ieee.org/document/{match.group(1)}"


def row_to_row(raw):
    return {
        "source": "IEEE Xplore",
        "title": clean_text(raw.get("Document Title", "")),
        "authors": clean_text(raw.get("Authors", "")),
        "year": clean_text(raw.get("Publication Year", "")),
        "venue": clean_text(raw.get("Publication Title", "")),
        "doi": clean_text(raw.get("DOI", "")),
        "url": document_url(raw.get("PDF Link", "")),
        "abstract": clean_text(raw.get("Abstract", "")),
    }


def parse_csv(input_file):
    with open(input_file, newline="", encoding="utf-8-sig") as f:
        raw_rows = list(csv.DictReader(f))

    print(f"[IEEE Xplore] parsing {len(raw_rows)} rows from {input_file}")

    rows = []
    for raw in raw_rows:
        year_str = raw.get("Publication Year", "").strip()
        if year_str.isdigit() and not (YEAR_FROM <= int(year_str) <= YEAR_TO):
            print(f"  skipping '{raw.get('Document Title', '')[:60]}' (year {year_str} out of range)")
            continue
        rows.append(row_to_row(raw))
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
        help=f"CSV file exported from IEEE Xplore (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output folder (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    rows = parse_csv(args.input)
    write_csv(os.path.join(args.out, "1_ieee_xplore.csv"), rows)


if __name__ == "__main__":
    main()
