# Screening Process

This document traces the records from the merged search results in `screening_process/2_merged.csv` to the final primary-study corpus in `screening_process/6_full_text_screening_included.csv`.

The authors manually performed deduplication, title screening, and abstract screening with support from Claude Sonnet 5 (Anthropic). For each stage, they documented the eligibility criteria and decision rules, and the assistant applied them record by record to the relevant titles or abstracts under the authors' review. The authors resolved every ambiguous or borderline case and made all final decisions.

The authors conducted the full-text stage entirely manually, reading every candidate PDF without AI assistance. The private working notes used during the AI-assisted stages are not part of the released package.

## Deduplication

**Input:** `2_merged.csv` (1,146 records from seven source-specific searches)  
**Output:** `3_deduplicated.csv` (766 records)

The same paper often appeared in several databases or more than once in a single database. Google Scholar, in particular, sometimes truncated titles and author lists with “…”. Two records were treated as the same paper when:

1. they shared the same normalized DOI (with `https://doi.org/` or `http://dx.doi.org/` removed and letter case ignored); or
2. in the absence of a shared DOI, their normalized titles matched exactly or one was a clean prefix of the other. Title normalization converted text to lowercase, removed punctuation, and discarded trailing “…” truncation. Publication years also had to match or be consistent with a preprint-to-camera-ready interval; author overlap was checked when needed.

Records were never merged on topical similarity alone. In each duplicate group, the `source` field lists all contributing sources once and in alphabetical order (for example, `ACM Digital Library; arXiv; Google Scholar`). Each remaining field takes the most complete value available within the group: a full title, author list, or abstract rather than a truncated one; a non-empty DOI rather than an empty value; and a canonical publisher venue or year rather than its preprint counterpart. No value was introduced from outside the group. Unique records passed through unchanged.

This stage reduced 1,146 records to 766 distinct papers.

## Title screening

**Input:** `3_deduplicated.csv` (766 records), screened by title only  
**Output:** `4_title_screening_included.csv` (143 records) and `4_title_screening_excluded.csv` (623 records, each with a `reason_for_exclusion`)

Title screening was the broadest and most permissive filter. A record was excluded only when its title made the mismatch with the review scope unambiguous; uncertain cases proceeded to abstract screening. Exclusion reasons were:

- **Wrong artifact or medium:** watermarking of images, video, audio, 3D objects, QR codes, documents, biometrics, databases, vector maps, or other non-code content. This was the most common reason because generic search terms also retrieved unrelated work in which “watermarking” co-occurred with terms such as error-correction “coding,” QR “codes,” or barcodes.
- **Wrong substrate:** watermarking of hardware description languages such as RTL, Verilog, or VHDL rather than software source code.
- **Wrong content type:** watermarking of natural language or text only, with no code component.
- **Passive-only method:** detection or classification of machine-generated code without embedding a signal.

Two questions were deliberately deferred because titles rarely answer them reliably: what artifact the method actually verifies, and whether conventionally worded software-watermarking work has any generative-AI connection. Titles that mentioned a model, dataset, or API were not assumed to establish the verification target, and apparently conventional methods were not excluded solely for lacking an explicit LLM reference in the title. Surveys and independent evaluations also remained at this stage.

## Abstract screening

**Input:** `4_title_screening_included.csv` (143 records). Google Scholar abstracts truncated with “…” were first completed manually from the original arXiv or publisher source.  
**Output:** `5_abstract_screening_included.csv` (31 records) and `5_abstract_screening_excluded.csv` (112 records, each with a `reason_for_exclusion`)

Each title and complete abstract was assessed in this order:

1. **Method contribution:** Does the work introduce or substantially adapt a watermarking method? Surveys, independent evaluations, attack or removal studies, purification studies, and benchmarks without a method of their own were classified as secondary or contextual studies. They remained relevant to the review but were not primary method contributions.
2. **Artifact and verification target:** Does the method embed a signal in generated code and verify it by examining that artifact? Methods that instead verify model parameters or weights, a fine-tuned tokenizer, a training dataset, an API or service, an agent's behavior, or an identity other than the LLM as source were excluded. The exception was a code corpus directly connected to the LLM code-watermarking literature.
3. **Source-code and generative-AI scope:** Is the artifact software source code with a connection to LLMs or generative AI? Natural-language-only work, hardware watermarking, and conventional pre-LLM software watermarking without such a connection were excluded.
4. **Inclusion:** Records that passed the preceding checks proceeded to full-text screening.

Most records retained at title stage because of ambiguous model, dataset, or API language were resolved as out of scope once their abstracts were examined. This outcome reflects the deliberately permissive title screen.

## Full-text screening

**Input:** `5_abstract_screening_included.csv` (31 records) and the corresponding PDFs archived under `local/` as private, unreleased working material  
**Output:** `6_full_text_screening_included.csv` (21 records, each with an `inclusion_reason` and qualitative `evaluation`) and `6_full_text_screening_excluded.csv` (10 records, each with an `exclusion_reason`)

The authors read every paper in full to assess three issues that could not always be resolved from the abstract:

1. **Duplicate or earlier versions:** A preprint and a later peer-reviewed version—sometimes retitled or extended—could both reach this stage. When two records represented the same underlying work, the more recent, complete, or peer-reviewed version was retained.
2. **Verification target:** The method section could reveal that an apparent code-artifact watermark instead operated at dataset level, verified by querying a downstream model, or at model level, protecting the model, API, or service. Both were outside scope even when motivated by code-generation protection.
3. **Integrity of technical claims:** Citations were spot-checked for accuracy and relevance, while results were checked for traceability to a described method, dataset, and baseline. Papers with fabricated or misattributed citations, or results that could not be linked to a described experiment, were excluded regardless of topical fit.

Non-peer-reviewed work, including preprints and technical reports, also had to provide enough technical and experimental detail for independent assessment.

Each included record received a two-to-four-sentence `inclusion_reason` describing the method, embedding and verification mechanism, and publication status. Its qualitative `evaluation`, scored out of 10, assesses the clarity of the objective and the strength of the supporting evidence: resources, models, languages, baselines, metrics, and attack or robustness protocols. This matches the manuscript's qualitative quality-assessment approach and is not a numerical risk-of-bias score.

The final corpus contains **21 primary studies**.
