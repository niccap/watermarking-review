# Supplementary Material

This repository contains the supplementary material for the systematic literature review **“Watermarking LLM-Generated Code: A Systematic Literature Review of Methods, Evaluation Practices, and Research Challenges.”**

## Scope

The repository provides a transparent—and, where database access permits, reproducible—record of the review process. It covers:

- database-specific search strings, dates, and retrieved records;
- record merging, deduplication, and screening decisions;
- secondary studies and backward and forward snowballing;
- data extracted from the final primary studies;
- data and scripts used to produce the article's tables, figures, and aggregate results.

Bibliographic databases change over time and may require subscriptions or interactive access, so rerunning a query may not reproduce the archived results exactly. The CSV files preserve the search and screening audit trail.

## Repository structure

```text
.
├── README.md
├── search_strings.md
├── screening_process.md
├── scripts/
│   ├── query_<source>.py
│   ├── query_and_merge.py
│   ├── merge_citations.py
│   └── raw_data/
├── screening_process/
│   ├── 1_<source>.csv
│   ├── 2_merged.csv
│   ├── 3_deduplicated.csv
│   ├── 4_title_screening_{included,excluded}.csv
│   ├── 5_abstract_screening_{included,excluded}.csv
│   ├── 6_full_text_screening_{included,excluded}.csv
│   ├── secondary_studies.csv
│   └── snowballing.csv
├── data_extraction/
│   ├── 1_primary_studies.csv
│   ├── 2_primary_studies_audit.csv
│   ├── 3_methods.csv
│   ├── 4_resources.csv
│   ├── 5_resource_usage.csv
│   ├── 6_quality_evaluation.csv
│   ├── 7_robustness_protocols.csv
│   └── 8_robustness_protocol_application.csv
└── analysis/                       # planned
    ├── derived_counts.csv
    ├── table_data/
    └── figure_data/
```

## Search documentation

[`search_strings.md`](search_strings.md) records the search date, source-specific queries, and result counts. It also documents the publication-period restrictions (2022 onward), the **PDF** document-type criterion, and the **English-language** restriction.

Each scholarly source has a dedicated `scripts/query_<source>.py` script. All scripts write to a [`screening_process/1_<source>.csv`](screening_process/) file using the same eight-column schema: `source, title, authors, year, venue, doi, url, abstract`.

Because none of the seven sources offers both a public API and an official structured export, the scripts use the best available channel:

- `query_arxiv.py` queries the arXiv API and paginates until results fall outside the publication window.
- `query_google_scholar.py` parses manually saved result pages, archived in `scripts/raw_data/google_scholar/`, because Google Scholar has no public API and restricts automated queries.
- `query_acm_digital_library.py`, `query_science_direct.py`, and `query_scopus.py` parse archived BibTeX exports from manual searches.
- `query_ieee_xplore.py` and `query_springer_link.py` parse archived CSV exports from manual searches.

The scripts apply the publication-period filter documented in `search_strings.md` and share conventions for DOI normalization, HTML entity and whitespace cleanup, and—where relevant—LaTeX-to-Unicode conversion. `query_and_merge.py` runs all seven scripts followed by `merge_citations.py`, which concatenates their outputs into [`screening_process/2_merged.csv`](screening_process/2_merged.csv) without deduplication.

## Screening process

The numeric prefixes in `screening_process/` reflect the order of the selection pipeline. [`screening_process.md`](screening_process.md) documents the eligibility criteria and decision rules used for deduplication and screening.

### Stage 1: source-specific results

The [`1_<source>.csv`](screening_process/) files preserve the records retrieved from each database before cross-source merging. Their common fields are:

- `source`: database from which the record was retrieved;
- `title`: publication title;
- `authors`: author names as exported or retrieved;
- `year`: publication year;
- `venue`: journal, conference, repository, or other venue;
- `doi`: DOI, when available;
- `url`: record or publication URL;
- `abstract`: abstract or source-provided description, when available.

### Stage 2: merged records

[`2_merged.csv`](screening_process/2_merged.csv) combines all Stage 1 records without removing publications returned by multiple sources.

### Stage 3: deduplicated records

[`3_deduplicated.csv`](screening_process/3_deduplicated.csv) contains one reconciled record per publication. When a publication appears in multiple databases, its `source` field lists all contributing sources alphabetically.

The authors performed deduplication manually with support from Claude Sonnet 5, primarily using DOI and normalized-title matching. They reviewed publication-version matches and ambiguous cases themselves. See [Stage 3 in `screening_process.md`](screening_process.md#stage-3-deduplication) for the complete rules.

### Stage 4: title screening

- [`4_title_screening_included.csv`](screening_process/4_title_screening_included.csv) contains records retained for abstract screening. Google Scholar abstracts truncated with “…” were completed manually from the original source before Stage 5.
- [`4_title_screening_excluded.csv`](screening_process/4_title_screening_excluded.csv) contains excluded records and their `reason_for_exclusion`.

The authors performed title screening manually with support from Claude Sonnet 5. The [Stage 4 documentation](screening_process.md#stage-4-title-screening) describes the eligibility criteria.

### Stage 5: abstract screening

- [`5_abstract_screening_included.csv`](screening_process/5_abstract_screening_included.csv) contains records retained for full-text assessment.
- [`5_abstract_screening_excluded.csv`](screening_process/5_abstract_screening_excluded.csv) contains excluded records and their `reason_for_exclusion`.

The authors performed abstract screening manually with support from Claude Sonnet 5. The [Stage 5 documentation](screening_process.md#stage-5-abstract-screening) gives the criteria.

### Stage 6: full-text assessment

- [`6_full_text_screening_included.csv`](screening_process/6_full_text_screening_included.csv) contains the retained studies, with an `inclusion_reason` and a brief `evaluation` note.
- [`6_full_text_screening_excluded.csv`](screening_process/6_full_text_screening_excluded.csv) contains excluded studies and their `exclusion_reason`.

The authors performed full-text screening manually. The [Stage 6 documentation](screening_process.md#stage-6-full-text-screening) covers duplicate and version detection, confirmation of the verification target, and checks on citation and result integrity.

All final primary studies came from database searches. Snowballing served as a completeness check but added no new primary studies; superseded versions are identified separately in the screening records.

### Secondary studies and snowballing

[`secondary_studies.csv`](screening_process/secondary_studies.csv) records reviews, mapping studies, and independent evaluations used for context, comparison, or search-completeness checks. They are not counted as primary studies unless they independently meet the primary-study eligibility criteria.

[`snowballing.csv`](screening_process/snowballing.csv) records candidates found through backward and forward snowballing, along with their screening status and decision rationale. Candidates that were not added to the final corpus were outside scope, alternate versions of papers already considered, or secondary studies.

## Data extraction

The `data_extraction/` directory contains the canonical study index and structured evidence used to answer the research questions. For files 2–8, numeric prefixes correspond to the article's table numbers. Each `source_location` points to the relevant primary-study PDF in `local/primary_studies/`, not to the review manuscript.

- [`1_primary_studies.csv`](data_extraction/1_primary_studies.csv): stable study identifiers (`PS01`–`PS21`) and definitive bibliographic information.
- [`2_primary_studies_audit.csv`](data_extraction/2_primary_studies_audit.csv): evidence-backed study-level judgments across five methodological and reporting criteria, plus an overall decision.
- [`3_methods.csv`](data_extraction/3_methods.csv): one row per method (`M01`–`M21`), covering embedding, payload and signal design, verification, access assumptions, and key requirements.
- [`4_resources.csv`](data_extraction/4_resources.csv): datasets and benchmarks (`R01`–`R22`), including language coverage, available artifacts, scale, and type.
- [`5_resource_usage.csv`](data_extraction/5_resource_usage.csv): many-to-many links between resources and methods, with use roles, languages, splits, and notes.
- [`6_quality_evaluation.csv`](data_extraction/6_quality_evaluation.csv): method-level evaluation evidence for detectability, functional preservation, robustness, imperceptibility, efficiency, and capacity.
- [`7_robustness_protocols.csv`](data_extraction/7_robustness_protocols.csv): deduplicated catalog of attack and robustness protocols (`RP01`–`RP15`).
- [`8_robustness_protocol_application.csv`](data_extraction/8_robustness_protocol_application.csv): method-specific applications of those protocols, including intensity, tools or models, attacker knowledge, and post-attack outcomes.

Stable identifiers connect studies, methods, resources, protocols, and experiments across the repository. `study_id`, `method_id`, `resource_id`, and `protocol_id` are the main cross-file keys; identifiers prefixed with `U`, `QE`, `RPA`, and `QA` denote resource uses, quality-evaluation summaries, protocol applications, and quality assessments.

Categorical fields use lowercase snake case, and multi-valued fields use semicolon-separated values. `not_reported` indicates that the primary paper does not provide a value; `not_applicable` indicates that the field does not apply. Boolean evidence fields use `yes` and `no`, except when a primary study explicitly leaves an issue unresolved.

Each `source_location` has been reconciled with the archived PDF and cites its file name and relevant section, subsection, or table. Page numbers are omitted because pagination is not consistent across publisher copies and preprints.

[`6_quality_evaluation.csv`](data_extraction/6_quality_evaluation.csv) summarizes methods rather than individual experiments. Its `*_evaluated` fields indicate whether a dimension was assessed quantitatively; the corresponding `*_measures` fields report representative values in their original units. Supporting fields retain baselines, operating points, and experimental context. The file neither pools estimates nor assumes that similarly named measures are directly comparable. In particular, an attack described as semantics-preserving is not treated as post-attack functional validation unless the study reports a measured execution, test, syntax, or joint-quality outcome.

[`2_primary_studies_audit.csv`](data_extraction/2_primary_studies_audit.csv) follows the qualitative approach described in Section 4.2 of the manuscript: its judgments are evidence-backed inclusion assessments, not numerical risk-of-bias scores.

The robustness files separate taxonomy from application. [`7_robustness_protocols.csv`](data_extraction/7_robustness_protocols.csv) defines each protocol once; [`8_robustness_protocol_application.csv`](data_extraction/8_robustness_protocol_application.csv) records how each method applies it and which outcomes are measured again after the attack. A method tested against several protocols therefore has one application row per protocol.

## Planned artifacts

The planned `analysis/` directory will contain only outputs derived from the frozen screening and extraction data, including:

- aggregate counts reported in the article;
- table-ready evidence summaries;
- figure-ready data for the selection flow, publication timeline, design-space overview, and resource and language coverage;
- scripts or commands needed to regenerate these artifacts.

Where practical, each article table and figure will be linked to its source file and generation command.
