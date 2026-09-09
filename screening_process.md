# Screening Process

This document describes how records were carried from the merged search results in
`screening_process/2_merged.csv` to the final primary-study corpus in
`screening_process/6_full_text_screening_included.csv`. Deduplication and the title and abstract
screening stages were performed **manually by the authors**, with the support of
**Claude Sonnet 5** (Anthropic) as an AI assistant: for each of these stages, the authors defined
the eligibility criteria and decision rules in writing, and the assistant applied them record by
record (reading titles or abstracts as appropriate for the stage) under the authors' review. The
final, full-text screening stage was carried out **entirely manually by the authors**, who read
every candidate PDF themselves, without AI assistance. Throughout, the authors resolved ambiguous
or borderline cases and made the final call. This document summarizes the criteria actually
applied at each stage, for transparency and auditability; the working notes used for the
AI-assisted stages are private working material and are not part of the released package.

## Stage 3: Deduplication

**Input:** `2_merged.csv` (1146 records, the concatenation of all seven per-source searches).
**Output:** `3_deduplicated.csv` (766 records).

The same paper frequently appears more than once: indexed by several databases, or by the same
database more than once with different formatting (Google Scholar in particular truncates titles
and author lists with "…"). Two records were treated as the same paper when:

1. they shared the same DOI (normalized: `https://doi.org/` / `http://dx.doi.org/` prefixes
   stripped, case-insensitive); or, failing that,
2. their normalized titles (lowercased, punctuation stripped, trailing "…" truncation removed)
   matched exactly, or one was a clean prefix of the other, and the publication years were equal
   or consistent with a preprint-to-camera-ready gap — cross-checked against author overlap when
   in doubt.

Records were never merged on topical similarity alone. For each duplicate group, the `source`
field lists every contributing source, deduplicated and sorted alphabetically (e.g. `ACM Digital
Library; arXiv; Google Scholar`); every other field independently takes the most complete value
available anywhere in the group (a full title/author list/abstract over a truncated one, a
non-empty DOI over an empty one, the canonical publisher venue/year over a preprint's when both
exist) — never a value invented outside the group. Records with no duplicate pass through
unchanged. This step merged 1146 records into 766 distinct papers.

## Stage 4: Title screening

**Input:** `3_deduplicated.csv` (766 records), screened by **title only**.
**Output:** `4_title_screening_included.csv` (143 records) and `4_title_screening_excluded.csv`
(623 records, with a `reason_for_exclusion`).

This stage is deliberately the coarsest, most permissive filter in the pipeline: it excludes a
title only when it is *unambiguous* that the paper falls outside scope, and defers every harder
judgment call to abstract screening. A record was excluded at this stage only for:

- **Wrong artifact/medium** — watermarking of images, video, audio, 3D objects, QR codes,
  documents, biometrics, databases, vector maps, or other non-code content. This is by far the
  most common exclusion reason: the search terms are generic enough that a large body of unrelated
  digital-watermarking work matches "watermark(ing)" and "code"/"program" purely by coincidence
  (error-correction "coding", QR "codes", barcodes, and similar false-positive terminology).
- **Wrong substrate** — hardware-description-language (RTL/Verilog/VHDL) watermarking, a
  different artifact than software source code.
- **Wrong content type** — natural-language/text-only LLM watermarking with no code angle.
- **Passive-only methods** — detectors/classifiers that identify machine-generated code without
  embedding any signal.

Two categories were explicitly *not* decided at title stage, because a title alone rarely settles
them reliably: (a) the actual **verification target** (a title mentioning "model", "dataset", or
"API" does not by itself establish what the paper verifies), and (b) whether a conventionally
worded software/code-watermarking title genuinely has **no generative-AI connection** — both were
left for abstract screening, where the full text is available. Titles that merely said "survey" or
described an independent evaluation were kept in at this stage as well.

## Stage 5: Abstract screening

**Input:** `4_title_screening_included.csv` (143 records) — with the abstracts Google Scholar had
truncated with "…" manually completed from the original source (arXiv, publisher page) beforehand,
so every record was screened against a complete abstract, not a cut-off one.
**Output:** `5_abstract_screening_included.csv` (31 records) and
`5_abstract_screening_excluded.csv` (112 records, with a `reason_for_exclusion`).

Each record was read in full (title + abstract) and evaluated in order against four questions:

1. Does it introduce or substantially adapt a watermarking **method**? Surveys, independent
   empirical evaluations of existing methods, attack/removal/purification studies, and benchmarks
   that don't propose a method of their own were excluded here as **secondary/contextual studies**
   — not because they're irrelevant, but because they don't count as primary method contributions.
2. Does that method embed a signal in a **generated code artifact** and verify it **by examining
   that artifact**? This resolved the verification-target question deferred from title screening:
   excluded here are methods that, on reading the abstract, turn out to verify the model itself
   (parameters, weights, a fine-tuned tokenizer), the training dataset (unless it is itself a code
   corpus tied to the LLM-code-watermarking literature), an API/service, an agent's behavior, or an
   identity other than "the LLM as source" (e.g. which user or student submitted something).
3. Is the artifact genuinely software source code with some connection to LLMs/generative AI,
   confirmed from the abstract — as opposed to natural-language-only content, a hardware substrate,
   or conventional (pre-LLM) software watermarking with no generative-AI angle anywhere in the
   abstract?
4. Otherwise, include.

Nearly all of the records deferred from title screening for an ambiguous "model"/"dataset"/"API"
framing were resolved as out of scope at this stage once the full abstract was read — confirming
that title screening's permissiveness did not silently smuggle ineligible work past the pipeline.

## Stage 6: Full-text screening

**Input:** `5_abstract_screening_included.csv` (31 records) and the corresponding 31 PDFs archived
under `local/` (private working material, not released).
**Output:** `6_full_text_screening_included.csv` (21 records, with an `inclusion_reason` and a
qualitative `evaluation`) and `6_full_text_screening_excluded.csv` (10 records, with an
`exclusion_reason`).

This is the last and most rigorous stage: each paper was read in full, because three things only
surface once the whole text is available:

1. **Duplicate or earlier version of another paper in the same set of 31.** An arXiv preprint and
   its later peer-reviewed publication (sometimes retitled or extended) can both survive
   independently to this stage; when two records were the same underlying work, the more
   recent/complete/peer-reviewed one was kept and the other excluded as a duplicate.
2. **Re-confirmation of the verification target.** The full method section sometimes reveals that
   what read as a code-artifact watermark from the abstract is actually a dataset-level watermark
   (verified by statistically querying a suspect downstream model, not by inspecting generated
   code) or a model-level watermark (protects the model/API/service itself) — both out of scope
   even when the paper's stated motivation is protecting "a code-generation model."
3. **Whether the paper's technical claims can be trusted.** Citations were spot-checked for
   accuracy and topical relevance, and reported results for traceability to a described method,
   dataset, and baseline; a paper with fabricated or misattributed citations, or results that could
   not be traced to any described experiment, was excluded regardless of topical fit.

Non-peer-reviewed work (preprints, technical reports) was additionally required to carry enough
technical/experimental detail to be assessed on its own terms. Included records were annotated
with a 2-4 sentence `inclusion_reason` naming the method, its embedding/verification mechanism,
and its publication status, and a qualitative `evaluation` score out of 10 judging the clarity of
the objective and the strength of the supporting evidence (resources, models, languages,
baselines, metrics, and attack/robustness protocols) — the same qualitative approach the review's
manuscript uses for quality assessment, rather than a numerical risk-of-bias score.

This stage yielded the final primary-study corpus of **21 studies**.
