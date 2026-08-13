# Vision Benchmark — 2026-08-13_sonnet-16k

**BENCHMARK_AGAINST_PREFREEZE_TRUTH** — truth is AI-reconciled,
human-unverified; rerun after researcher sign-off changes any value.

Provider: live · role OVERRIDE(COMPLEX_EXTRACTION_MODEL) → `claude-sonnet-5` · prompt v1

Headline metric: FULL_ROW_EXACT_MATCH ('Row asm' below) — label +
effect + CI pair + weight (where truth has one) all correct
simultaneously for a truth study row.

## Per paper

| Paper | Recall | Precision | Label | Numeric | CI pair | FULL ROW | Pooled misclass | False extr | Inappr. resolve | Abstain | Prov. page | Cost | Latency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hahn-2024-exercise-intake | 100.0% | 35.1% | 100.0% | 0.0%/100.0% | 83.3% | **0.0%** | 0 | 0 | 0 | 0 | 73.6% | $0.6674 | 270417ms |
| driessen-2015-nih-psychotherapy | 94.4% | 94.4% | 100.0% | 100.0%/100.0% | 96.4% | **94.0%** | 0 | 4 | 0 | 9 | 100.0% | $0.5146 | 213257ms |

### By region kind

- hahn-2024-exercise-intake · VECTOR_CLUSTER: 6 region(s), 256 rows extracted
- driessen-2015-nih-psychotherapy · RASTER_IMAGE: 6 region(s), 109 rows extracted

## Aggregate (secondary to per-paper)

- study-row recall 96.9%, precision 53.1%
- among matched: label 100.0%, numeric 53.8%, CI 90.4%, full row 50.6%
- pooled misclassified 0, false extractions 4

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

