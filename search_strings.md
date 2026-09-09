# Search Strings

Search date: **2026-09-08 – 2026-09-09**

Publication period covered: **2022–2026** (ACM Digital Library, arXiv, IEEE Xplore); **2022 onwards, no upper bound**, to avoid dropping early-access/in-press records dated into next year

Document type: **PDF**

Language: **English**

The queries below are adapted to the syntax and search fields supported by each scholarly source. Where supported, the publication period, document type, and language were applied through the source's filters. The reported counts are the numbers of records retrieved on the search date, before cross-source merging and deduplication, as produced by the corresponding `scripts/query_*.py` script (see `README.md`).

## ACM Digital Library

Results: **39**

```text
Title:(watermark OR watermarking) AND All:(code OR "source code" OR program OR programming) AND All:(LLM OR "large language model" OR "generative AI")
```

## arXiv

Results: **117**

```text
ti:(watermark OR watermarking) AND all:(code OR "source code" OR program OR programming) AND all:(LLM OR "large language model" OR "generative AI")
```

## Google Scholar

Results: **416**

```text
(intitle:watermark OR intitle:watermarking) AND (intitle:code OR intitle:'source code' OR intitle:program OR intitle:programming) AND (LLM OR 'large language model' OR 'generative AI')
```

## IEEE Xplore

Results: **116**

```text
("Document Title":watermark OR "Document Title":watermarking) AND ("Full Text & Metadata":code OR "Full Text & Metadata":"source code" OR "Full Text & Metadata":program OR "Full Text & Metadata":programming) AND ("Full Text & Metadata":LLM OR "Full Text & Metadata":"large language model" OR "Full Text & Metadata":"generative AI")
```

## ScienceDirect

Results: **117**

ScienceDirect splits the query across two separate search boxes rather than a single boolean string:

```text
Find articles with these terms: (code OR "source code" OR program OR programming) AND (LLM OR "large language model" OR "generative AI")
Title: watermark OR watermarking
```

## Scopus

Results: **302**

```text
TITLE(watermark OR watermarking) AND ALL(code OR "source code" OR program OR programming) AND ALL(LLM OR "large language model" OR "generative AI") AND PUBYEAR > 2021
```

## SpringerLink

Results: **39**

SpringerLink splits the query across two separate search boxes rather than a single boolean string:

```text
Keywords: (code OR "source code" OR program OR programming) AND (LLM OR "large language model" OR "generative AI")
Title: watermark OR watermarking
```

Published from 2022 onwards.
