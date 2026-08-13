# Vision Benchmark — 2026-08-13_sonnet-final

**BENCHMARK_AGAINST_PREFREEZE_TRUTH** — truth is AI-reconciled,
human-unverified; rerun after researcher sign-off changes any value.

Provider: replay · role OVERRIDE(COMPLEX_EXTRACTION_MODEL) → `claude-sonnet-5` · prompt v1

Headline metric: FULL_ROW_EXACT_MATCH ('Row asm' below) — label +
effect + CI pair + weight (where truth has one) all correct
simultaneously for a truth study row.

## Per paper

| Paper | Recall | Precision | Label | Numeric | CI pair | FULL ROW | Pooled misclass | False extr | Inappr. resolve | Abstain | Prov. page | Cost | Latency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| yang-2018-sii | 100.0% | 100.0% | 100.0% | 100.0%/100.0% | 100.0% | **100.0%** | 0 | 0 | 0 | 0 | 100.0% | $0 | 0ms |
| prochaska-2012-varenicline | 100.0% | 97.7% | 100.0% | 100.0%/100.0% | 100.0% | **100.0%** | 2 | 0 | 0 | 0 | 100.0% | $0 | 0ms |
| hahn-2024-exercise-intake | 100.0% | 35.1% | 100.0% | 0.0%/100.0% | 100.0% | **100.0%** | 0 | 0 | 0 | 0 | 100.0% | $0 | 0ms |
| driessen-2015-nih-psychotherapy | 94.4% | 94.4% | 100.0% | 100.0%/100.0% | 96.4% | **94.0%** | 0 | 4 | 0 | 9 | 100.0% | $0 | 0ms |

### By region kind

- yang-2018-sii · RASTER_IMAGE: 2 region(s), 45 rows extracted
- prochaska-2012-varenicline · RASTER_IMAGE: 3 region(s), 48 rows extracted
- hahn-2024-exercise-intake · VECTOR_CLUSTER: 6 region(s), 256 rows extracted
- driessen-2015-nih-psychotherapy · RASTER_IMAGE: 6 region(s), 109 rows extracted

## Aggregate (secondary to per-paper)

- study-row recall 97.9%, precision 62.6%
- among matched: label 100.0%, numeric 69.1%, CI 98.7%, full row 97.9%
- pooled misclassified 2, false extractions 4

## Examples

### driessen-2015-nih-psychotherapy
- missed: [unnamed unpublished] 0.31 (p13)
- missed: [unnamed unpublished] 0.31 (p14)
- missed: [unnamed unpublished] 0.44 (p14)
- missed: [unnamed unpublished] -0.24 (p14)
- missed: [unnamed unpublished] 0.56 (p15)
- false:  0,31 (p14)
- false: UNRESOLVED 0,44 (p14)
- false: UNRESOLVED -0,24 (p14)
- false: Unpublished 0,56 (p15)

