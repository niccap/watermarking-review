#!/usr/bin/env python3
"""
query_arxiv.py

Queries the official arXiv API with the boolean query:

  ti:(watermark OR watermarking)
  AND all:(code OR "source code" OR program OR programming)
  AND all:(LLM OR "large language model" OR "generative AI")

and saves the results to screening_process/1_arxiv.csv using the same
schema as the other CSV files in the project: source, title, authors,
year, venue, doi, url, abstract.

Usage:
  python3 query_arxiv.py --out screening_process/
"""

import argparse
import csv
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

CODE_TERMS = ["code", "source code", "program", "programming"]
WATERMARK_TERMS = ["watermark", "watermarking"]
LLM_TERMS = ["LLM", "large language model", "generative AI"]

YEAR_FROM = 2022
YEAR_TO = 2026

FIELDNAMES = ["source", "title", "authors", "year", "venue", "doi", "url", "abstract"]

DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (systematic-review-script; contact: ncapuano@unisa.it)"}


def http_get_xml(url, headers=None, retries=3, backoff=2.0):
    headers = {**DEFAULT_HEADERS, **(headers or {})}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return ET.fromstring(resp.read())
        except Exception as e:
            if attempt == retries - 1:
                raise
            print(f"    retrying ({e})...")
            time.sleep(backoff * (attempt + 1))


def field_or(terms):
    return " OR ".join(f'"{t}"' if " " in t else t for t in terms)


def build_search_query():
    wm_group = f"ti:({field_or(WATERMARK_TERMS)})"
    code_group = f"all:({field_or(CODE_TERMS)})"
    llm_group = f"all:({field_or(LLM_TERMS)})"
    return f"{wm_group} AND {code_group} AND {llm_group}"


def query_arxiv():
    search_query = build_search_query()
    print(f"[arXiv] query: {search_query}")
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    rows = []
    start = 0
    page_size = 100
    while True:
        params = {
            "search_query": search_query,
            "start": start,
            "max_results": page_size,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        root = http_get_xml(url)
        entries = root.findall("atom:entry", ns)
        if not entries:
            break
        for entry in entries:
            published = entry.findtext("atom:published", default="", namespaces=ns)
            year_str = published[:4]
            if not year_str.isdigit():
                continue
            year_num = int(year_str)
            if year_num < YEAR_FROM:
                # Results are sorted by submittedDate descending, so once we
                # reach a paper older than YEAR_FROM every remaining entry
                # (on this page and any further page) will be too.
                print(f"[arXiv] reached {year_num}, older than YEAR_FROM={YEAR_FROM}, stopping.")
                return rows
            if year_num > YEAR_TO:
                continue
            year = year_str
            title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip().replace("\n", " ")
            summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip().replace("\n", " ")
            authors = "; ".join(
                a.findtext("atom:name", default="", namespaces=ns)
                for a in entry.findall("atom:author", ns)
            )
            arxiv_url = entry.findtext("atom:id", default="", namespaces=ns)
            doi = entry.findtext("atom:doi", default="", namespaces={"atom": "http://arxiv.org/schemas/atom"}) or ""
            rows.append({
                "source": "arXiv",
                "title": title,
                "authors": authors,
                "year": year,
                "venue": "arXiv preprint",
                "doi": doi,
                "url": arxiv_url,
                "abstract": summary,
            })
        start += page_size
        if len(entries) < page_size:
            break
        time.sleep(1.0)
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
    parser.add_argument("--out", default="screening_process", help="Output folder (default: screening_process/)")
    args = parser.parse_args()

    rows = query_arxiv()
    write_csv(os.path.join(args.out, "1_arxiv.csv"), rows)


if __name__ == "__main__":
    main()
