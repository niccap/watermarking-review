#!/usr/bin/env python3
"""
query_springer_link.py

SpringerLink has no public search API, so this script does not query it
directly. Instead, it parses the CSV export of the manual search done on
the SpringerLink website using:

  Keywords:
    (code OR "source code" OR program OR programming)
    AND (LLM OR "large language model" OR "generative AI")

  Title:
    watermark OR watermarking

  Published from 2022 onwards.

(saved as scripts/raw_data/springer_link.csv), and extracts each row's
metadata into screening_process/1_springer_link.csv, using the same
schema as the other CSV files in the project: source, title, authors,
year, venue, doi, url, abstract.

Note on authors: SpringerLink's CSV export concatenates all author names
into a single string with NO delimiter between them (e.g. "Haibo LinZhong
LiRuihua Ji..." for "Haibo Lin, Zhong Li, Ruihua Ji, ..."), and the
export has no Abstract column at all. Splitting that string back into
individual names is ambiguous (it can't be done reliably without a name
dictionary), so the 'authors' field is left exactly as exported rather
than risking a wrong split; check the DOI/URL if you need the individual
authors for a given record.

Usage:
  python3 query_springer_link.py
  python3 query_springer_link.py --input raw_data/springer_link.csv --out screening_process
"""

import argparse
import csv
import html
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_INPUT_FILE = os.path.join(SCRIPT_DIR, "raw_data", "springer_link.csv")
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "screening_process")

YEAR_FROM = 2022

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]


def clean_text(value):
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def row_to_row(raw):
    venue = raw.get("Publication Title") or raw.get("Book Series Title") or ""
    return {
        "source": "SpringerLink",
        "title": clean_text(raw.get("Item Title", "")),
        "authors": clean_text(raw.get("Authors", "")),
        "year": clean_text(raw.get("Publication Year", "")),
        "venue": clean_text(venue),
        "doi": clean_text(raw.get("Item DOI", "")),
        "url": clean_text(raw.get("URL", "")),
        "abstract": "",
    }


def parse_csv(input_file):
    with open(input_file, newline="", encoding="utf-8-sig") as f:
        raw_rows = list(csv.DictReader(f))

    print(f"[SpringerLink] parsing {len(raw_rows)} rows from {input_file}")

    rows = []
    for raw in raw_rows:
        year_str = raw.get("Publication Year", "").strip()
        if year_str.isdigit() and int(year_str) < YEAR_FROM:
            print(f"  skipping '{raw.get('Item Title', '')[:60]}' (year {year_str} before {YEAR_FROM})")
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
        help=f"CSV file exported from SpringerLink (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output folder (default: {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    rows = parse_csv(args.input)
    write_csv(os.path.join(args.out, "1_springer_link.csv"), rows)


if __name__ == "__main__":
    main()
