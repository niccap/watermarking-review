#!/usr/bin/env python3
"""
query_and_merge.py

Runs all the per-source query_*.py scripts (each producing its own
screening_process/1_*.csv) and then merge_citations.py (producing
screening_process/2_merged.csv), in one go.

Each query script reads its own raw data (a saved HTML/BibTeX/CSV export
under scripts/raw_data/, or arXiv's live API for query_arxiv.py) and
writes its 1_*.csv independently of the others, so this is just a
convenience runner -- see each query_*.py's own docstring for what it
does and what input it expects.

Usage:
  python3 query_and_merge.py
"""

import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

QUERY_SCRIPTS = [
    "query_acm_digital_library.py",
    "query_arxiv.py",
    "query_google_scholar.py",
    "query_ieee_xplore.py",
    "query_science_direct.py",
    "query_scopus.py",
    "query_springer_link.py",
]

MERGE_SCRIPT = "merge_citations.py"


def run_script(name):
    path = os.path.join(SCRIPT_DIR, name)
    print(f"\n=== {name} ===", flush=True)
    result = subprocess.run([sys.executable, path])
    return result.returncode == 0


def main():
    failed = []
    for name in QUERY_SCRIPTS:
        if not run_script(name):
            failed.append(name)

    if failed:
        print(f"\n[query_and_merge] {len(failed)} script(s) failed: {', '.join(failed)}")
        print("[query_and_merge] skipping merge -- fix the failures above and rerun.")
        sys.exit(1)

    if not run_script(MERGE_SCRIPT):
        print("\n[query_and_merge] merge_citations.py failed.")
        sys.exit(1)

    print("\n[query_and_merge] done.")


if __name__ == "__main__":
    main()
