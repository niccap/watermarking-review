#!/usr/bin/env python3
"""
merge_citations.py

Concatenates all the per-source citation CSVs produced by the query_*.py
scripts (screening_process/1_*.csv) into a single file,
screening_process/2_merged.csv, using the project's standard schema:
source, title, authors, year, venue, doi, url, abstract.

This step does not deduplicate records across sources; that happens in
the next pipeline stage (3_deduplicated.csv).

Usage:
  python3 merge_citations.py
  python3 merge_citations.py --input screening_process --out screening_process
"""

import argparse
import csv
import glob
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DEFAULT_DIR = os.path.join(PROJECT_ROOT, "screening_process")

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]


def merge_csvs(input_dir):
    files = sorted(glob.glob(os.path.join(input_dir, "1_*.csv")))
    if not files:
        raise SystemExit(f"No 1_*.csv files found in {input_dir}")

    print(f"[merge] merging {len(files)} source files from {input_dir}")

    rows = []
    for path in files:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != FIELDNAMES:
                print(f"  WARNING: {os.path.basename(path)} has unexpected columns {reader.fieldnames}, skipping")
                continue
            file_rows = list(reader)
        print(f"  {os.path.basename(path)}: {len(file_rows)} records")
        rows.extend(file_rows)

    print(f"[merge] {len(rows)} records total")
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
        default=DEFAULT_DIR,
        help=f"Folder containing the 1_*.csv source files (default: {DEFAULT_DIR})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_DIR,
        help=f"Output folder (default: {DEFAULT_DIR})",
    )
    args = parser.parse_args()

    rows = merge_csvs(args.input)
    write_csv(os.path.join(args.out, "2_merged.csv"), rows)


if __name__ == "__main__":
    main()
