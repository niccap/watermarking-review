# Search Strings

- **Search date:** 2026-09-08
- **Publication period:** 2022 onward, with no upper bound, to retain early-access or in-press records dated into the following year
- **Document type:** PDF
- **Language:** English

The queries below reflect the syntax and search fields available in each scholarly source. Publication period, document type, and language were applied through source filters where supported. Result counts refer to records retrieved on the search date, before cross-source merging and deduplication, as produced by the corresponding `scripts/query_*.py` script described in [`README.md`](README.md).

## ACM Digital Library

**Results:** 39

```text
Title:(watermark OR watermarking) AND All:(code OR "source code" OR program OR programming) AND All:(LLM OR "large language model" OR "generative AI")
```

## arXiv

**Results:** 117

```text
ti:(watermark OR watermarking) AND all:(code OR "source code" OR program OR programming) AND all:(LLM OR "large language model" OR "generative AI")
```

## Google Scholar

**Results:** 416

```text
(intitle:watermark OR intitle:watermarking) AND (intitle:code OR intitle:'source code' OR intitle:program OR intitle:programming) AND (LLM OR 'large language model' OR 'generative AI')
```

## IEEE Xplore

**Results:** 116

```text
("Document Title":watermark OR "Document Title":watermarking) AND ("Full Text & Metadata":code OR "Full Text & Metadata":"source code" OR "Full Text & Metadata":program OR "Full Text & Metadata":programming) AND ("Full Text & Metadata":LLM OR "Full Text & Metadata":"large language model" OR "Full Text & Metadata":"generative AI")
```

## ScienceDirect

**Results:** 117

ScienceDirect divides the query between two search boxes:

```text
Find articles with these terms: (code OR "source code" OR program OR programming) AND (LLM OR "large language model" OR "generative AI")
Title: watermark OR watermarking
```

## Scopus

**Results:** 302

```text
TITLE(watermark OR watermarking) AND ALL(code OR "source code" OR program OR programming) AND ALL(LLM OR "large language model" OR "generative AI") AND PUBYEAR > 2021
```

## SpringerLink

**Results:** 39

SpringerLink divides the query between two search boxes:

```text
Keywords: (code OR "source code" OR program OR programming) AND (LLM OR "large language model" OR "generative AI")
Title: watermark OR watermarking
```

The publication filter was set to 2022 onward.
