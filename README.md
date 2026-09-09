# Supplementary Material

This repository contains the supplementary material for the systematic literature review **“Watermarking LLM-Generated Code: A Systematic Literature Review of Methods, Evaluation Practices, and Research Challenges.”**

The review and this repository are under active development. Consequently, the current records, study-selection decisions, counts, file names, and planned artifacts may change before publication. The final release will be aligned with the corresponding version of the article and archived as a versioned snapshot.

## Scope

The repository is intended to make the review process transparent and, where database access permits, reproducible. It documents:

- the database-specific search strings and search dates;
- the records retrieved from each scholarly source;
- merging and deduplication;
- title, abstract, and full-text screening decisions;
- secondary studies and backward/forward snowballing;
- the data extracted from the final primary studies;
- the data and scripts used to produce the tables, figures, and aggregate results reported in the article.

Bibliographic databases can change over time and may require subscriptions or interactive access. Therefore, rerunning a query may not return exactly the same records as the archived search. The CSV files in this repository will constitute the review's search and screening audit trail.

## Repository structure

```text
.
├── README.md
├── search_strings.md
├── screening_process.md
├── scripts/
│   ├── query_acm_digital_library.py
│   ├── query_arxiv.py
│   ├── query_google_scholar.py
│   ├── query_ieee_xplore.py
│   ├── query_science_direct.py
│   ├── query_scopus.py
│   ├── query_springer_link.py
│   ├── query_and_merge.py
│   ├── merge_citations.py
│   └── raw_data/                 
├── screening_process/
│   ├── 1_acm_digital_library.csv
│   ├── 1_arxiv.csv
│   ├── 1_google_scholar.csv
│   ├── 1_ieee_xplore.csv
│   ├── 1_science_direct.csv
│   ├── 1_scopus.csv
│   ├── 1_springer_link.csv
│   ├── 2_merged.csv
│   ├── 3_deduplicated.csv
│   ├── 4_title_screening_included.csv
│   ├── 4_title_screening_excluded.csv
│   ├── 5_abstract_screening_included.csv
│   ├── 5_abstract_screening_excluded.csv
│   ├── 6_full_text_screening_included.csv
│   ├── 6_full_text_screening_excluded.csv
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

### [`search_strings.md`](search_strings.md)

Records the search date, the publication-period restriction applied at each source (2022–2026 where the source's own filter supports an upper bound; 2022 onward otherwise), the **PDF** document-type criterion, the **English-language** restriction, the query adapted to each scholarly source, and the number of results returned.

### `scripts/`

Each source has a dedicated `query_<source>.py` script that writes its own `screening_process/1_<source>.csv` in the common eight-column schema (`source, title, authors, year, venue, doi, url, abstract`). None of the seven scholarly sources exposes both a public API and an official structured export, so each script takes whatever channel is actually available for that source, documented in its own module docstring:

- **`query_arxiv.py`** queries the arXiv API directly and paginates until results fall outside the publication-period window.
- **`query_google_scholar.py`** parses the HTML of Google Scholar result pages saved manually (Google Scholar has no API and aggressively blocks automated queries), archived under `scripts/raw_data/google_scholar/`.
- **`query_acm_digital_library.py`**, **`query_science_direct.py`**, and **`query_scopus.py`** parse a BibTeX export of the manual search from each database's website, archived under `scripts/raw_data/`.
- **`query_ieee_xplore.py`** and **`query_springer_link.py`** parse a CSV export of the manual search from each database's website, also archived under `scripts/raw_data/`.

All seven scripts apply the same publication-period filter documented in `search_strings.md` and share field-cleaning conventions (DOI normalization, HTML-entity/whitespace cleanup, LaTeX-to-Unicode conversion for BibTeX sources). `query_and_merge.py` runs all seven in sequence and then `merge_citations.py`, which concatenates their outputs into `screening_process/2_merged.csv` without deduplicating.

## Screening process

The numeric prefixes in `screening_process/` indicate the order of the selection pipeline. This section describes what each stage's files contain; see [`screening_process.md`](screening_process.md) for the eligibility criteria and decision rules actually applied at deduplication and at each screening stage.

### Stage 1: source-specific search results

The files named `1_<source>.csv` contain the records retrieved from each database before cross-source merging. Their common fields are:

- `source`: scholarly source from which the record was retrieved;
- `title`: publication title;
- `authors`: author names as exported or retrieved;
- `year`: publication year;
- `venue`: journal, conference, repository, or other venue;
- `doi`: DOI when available;
- `url`: record or publication URL;
- `abstract`: abstract or source-provided description when available.

These files preserve the results retrieved on the documented search date and constitute the input to the subsequent review stages.

### Stage 2: merged records

`2_merged.csv` combines all Stage 1 records into a single file without removing publications returned by more than one source.

### Stage 3: deduplicated records

`3_deduplicated.csv` contains one record for each publication after duplicate detection and reconciliation. When duplicates originate from multiple databases, the `source` field can contain more than one source, listed alphabetically.

Deduplication was performed manually by the authors with the support of Claude Sonnet 5, primarily via DOI and normalized-title matching; publication-version matches and ambiguous cases were reviewed and decided by the authors. See [`screening_process.md`](screening_process.md#stage-3-deduplication) for the matching and merging rules applied.

### Stage 4: title screening

- `4_title_screening_included.csv` contains records retained after title screening and passed to abstract screening. Abstracts that Google Scholar had truncated with "…" have been manually completed from the original source, used as the input to Stage 5.
- `4_title_screening_excluded.csv` contains excluded records and their `reason_for_exclusion`.

Title screening was performed manually by the authors with the support of Claude Sonnet 5; see [`screening_process.md`](screening_process.md#stage-4-title-screening) for the eligibility criteria applied.

### Stage 5: abstract screening

- `5_abstract_screening_included.csv` contains records retained after abstract screening and passed to full-text assessment.
- `5_abstract_screening_excluded.csv` contains excluded records and their `reason_for_exclusion`.

Abstract screening was performed manually by the authors with the support of Claude Sonnet 5; see [`screening_process.md`](screening_process.md#stage-5-abstract-screening) for the eligibility criteria applied.

### Stage 6: full-text assessment

- `6_full_text_screening_included.csv` contains studies retained after full-text assessment. The current file includes an `inclusion_reason` and a short `evaluation` note.
- `6_full_text_screening_excluded.csv` contains studies excluded after full-text inspection and an `exclusion_reason`.

Full-text screening was performed manually by the authors; see [`screening_process.md`](screening_process.md#stage-6-full-text-screening) for the criteria applied, including duplicate/version detection, re-confirmation of the verification target, and citation/result-integrity checks.

All studies retained at this stage were identified through database searching. Snowballing was used as a completeness check but did not add any new primary studies. Superseded versions of the same work are identified separately in the screening records.

### Secondary studies

`secondary_studies.csv` records reviews, mapping studies, and independent evaluations used for contextualization, comparison, or search-completeness checks. These publications are not counted as primary studies unless they independently satisfy the primary-study eligibility criteria.

### Snowballing

`snowballing.csv` is the register of candidates identified through backward and forward snowballing. Its fields describe the direction of discovery, screening status, and decision rationale.

Snowballing did not add any new primary studies to the final corpus. The identified candidates were either outside the review's scope, different versions of papers already considered, or secondary studies. The decision for each candidate is recorded in the file.

## Data-extraction

The `data_extraction/` directory contains the canonical study index and the structured evidence used to answer the research questions. The numeric prefixes track the article's table numbers (Tables 2–8); each file's `source_location` column cites the primary-study PDF (in `local/primary_studies/`) that the row was extracted from, not the review manuscript itself. Its files have the following roles:

- [`1. primary_studies.csv`](<data_extraction/1. primary_studies.csv>): stable study identifiers (`PS01`–`PS21`) and definitive bibliographic information for the current primary-study corpus;
- [`2_quality_assessment.csv`](data_extraction/2_quality_assessment.csv): study-level assessment of methodological and reporting quality across five criteria (objective; embedding/verification; resources, models, and languages; baselines and metrics; attack protocol), each with a judgment and an evidence-backed rationale, plus an overall decision;
- [`3_methods.csv`](data_extraction/3_methods.csv): one row per method (`M01`–`M21`) — embedding mechanism, key design principle, embedding stage, payload type, signal representation, verification procedure, access assumptions, and key/secret requirements;
- [`4_resources.csv`](data_extraction/4_resources.csv): datasets and benchmarks used across the primary studies (`R01`–`R21`) — category, language coverage, description/code/executable-test availability, scale, and artifact type;
- [`5_resource_usage.csv`](data_extraction/5_resource_usage.csv): many-to-many mapping between resources and methods (`resource_id`, `method_id`), including the use role, the languages actually used, sample/split details, and notes;
- [`6_quality_evaluation.csv`](data_extraction/6_quality_evaluation.csv): one row per method giving the representative detectability, functional-preservation, robustness, imperceptibility, efficiency, and capacity results that back the article's method-level evaluation table, together with whether each dimension was quantitatively evaluated, baselines, thresholds, and experimental-scope notes;
- [`7_robustness_protocols.csv`](data_extraction/7_robustness_protocols.csv): a deduplicated catalog of the distinct attack/robustness protocol types identified across the primary studies (`RP01`–`RP15`), each with a generic description, attack family (`routine_editing`, `cropping`, `dilution`, `watermark_discovery`, `adaptive_removal_or_rewatermarking`), and typical tools;
- [`8_robustness_protocol_application.csv`](data_extraction/8_robustness_protocol_application.csv): many-to-many mapping between protocols and methods (`protocol_id`, `method_id`) recording how each method actually operationalizes a given protocol (intensity, tool/model used), the assumed attacker knowledge, and which of detectability, functionality, and imperceptibility were measured post-attack;
- `method_publication_timeline.csv` *(planned)*: month-level publication history for every method represented in Figure 3, including its first public scientific appearance, later venue or publisher publication, latest public version, supporting URLs, date precision, and verification notes;
- `primary_pdf_audit.md` *(planned)*: reconciliation log between the structured extraction, the review manuscript, and the locally archived primary-study PDFs.

The files use stable identifiers so that the same study, method, resource, protocol, and experiment can be traced across screening, extraction, tables, and figures. `study_id`, `method_id`, `resource_id`, and `protocol_id` are the primary cross-file keys. Row identifiers prefixed with `U`, `QE`, `RPA`, and `QA` identify resource uses, quality-evaluation summaries, protocol applications, and quality assessments, respectively.

`method_publication_timeline.csv` *(planned)* is intended as the source table for the temporal information shown in Figure 3. `first_appearance_*` will identify the earliest publicly available scientific version found during verification: normally an arXiv preprint, or the conference presentation when no earlier public version was identified. `latest_publication_*` will identify the later online publication by the venue or publisher; when a study has no separate venue version, it will identify the latest available preprint version. Events in the same month, and studies without a distinct later publication event, are intended to have `figure3_marker_count=1`; other studies two markers.

The separate `latest_public_version_*` fields are intended to preserve revisions that postdate the venue publication without changing the semantics of Figure 3 — relevant, for example, to CodeIP and PromptMark, whose later arXiv versions postdate their venue events, and to ACW (Li), whose latest arXiv revision appeared shortly after its journal record in the same month. The file is also intended to record title changes, online-first dates that differ from issue years, and records for which only month-level precision could be verified, each explained in `verification_note` and linked to the corresponding archived primary-study PDF through `local_primary_pdf`.

Categorical fields use lowercase snake case. Multi-valued fields use semicolon-separated values within a CSV cell. `not_reported` means that the consulted primary paper does not provide the value. `not_applicable` means that the field does not apply to the method or evaluation. Boolean evidence fields use `yes` and `no`, except where the primary study explicitly leaves an issue unresolved. Every `source_location` cell has been reconciled against the archived primary-study PDF it documents and cites that PDF's filename together with the relevant section, subsection, or table — never the review manuscript's own numbering; page numbers were intentionally omitted because pagination is not comparable across sources (some PDFs carry the venue's absolute printed page numbers, others are self-paginated preprints). The planned `primary_pdf_audit.md` will log this reconciliation in detail.

`6_quality_evaluation.csv` is a method-level summary rather than an experiment-level results table. Its `*_evaluated` flags record whether each quality dimension is quantitatively evaluated, and the corresponding `*_measures` field then reports the representative value(s) — with the original units — that the article's method-level evaluation table draws on; `baselines`, `thresholds_or_operating_points`, and `experimental_scope_and_notes` add the material experimental conditions. It does not create pooled estimates or imply that similarly named measures are directly comparable. In particular, a claim that an attack is semantics-preserving is not coded as post-attack functional validation unless the study reports a measured execution, test, syntax, or joint quality outcome on attacked artifacts. `2_quality_assessment.csv` likewise preserves the qualitative approach described in Section 4.2 of the manuscript: judgments are evidence-backed inclusion assessments, not a numerical risk-of-bias score.

`7_robustness_protocols.csv` and `8_robustness_protocol_application.csv` separate the attack taxonomy from its use: the former defines each protocol once, generically; the latter records, per method, how that protocol was actually operationalized (intensity, tool or model, attacker knowledge) and which outcomes were re-measured after the attack. A method that tests several distinct protocols therefore has several rows in `8_robustness_protocol_application.csv`, one per protocol.

## Planned analysis artifacts

The planned `analysis/` directory will contain only data derived from the frozen screening and extraction files. It is expected to include:

- aggregate counts reported in the text;
- table-ready data for the article's evidence summaries;
- figure-ready data for the selection flow, publication timeline, design-space overview, and resource/language coverage;
- scripts or commands that regenerate these derived artifacts.

Where practical, each table and figure in the article will be mapped to its source file and generation command.

