# Vision Benchmark — 2026-08-13_haiku-16k

**BENCHMARK_AGAINST_PREFREEZE_TRUTH** — truth is AI-reconciled,
human-unverified; rerun after researcher sign-off changes any value.

Provider: live · role OVERRIDE(COMPLEX_EXTRACTION_MODEL) → `claude-haiku-4-5-20251001` · prompt v1

Headline metric: FULL_ROW_EXACT_MATCH ('Row asm' below) — label +
effect + CI pair + weight (where truth has one) all correct
simultaneously for a truth study row.

## Per paper

| Paper | Recall | Precision | Label | Numeric | CI pair | FULL ROW | Pooled misclass | False extr | Inappr. resolve | Abstain | Prov. page | Cost | Latency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hahn-2024-exercise-intake | 95.8% | 33.7% | 100.0% | 0.0%/100.0% | 98.6% | **95.7%** | 0 | 25 | 0 | 0 | 98.6% | $0.2488 | 271234ms |
| driessen-2015-nih-psychotherapy | 21.3% | 82.6% | 100.0% | 36.8%/36.8% | 31.6% | **15.8%** | 0 | 4 | 0 | 3 | 47.4% | $0.1697 | 217071ms |

### By region kind

- hahn-2024-exercise-intake · VECTOR_CLUSTER: 6 region(s), 243 rows extracted
- driessen-2015-nih-psychotherapy · RASTER_IMAGE: 6 region(s), 29 rows extracted

## Aggregate (secondary to per-paper)

- study-row recall 54.7%, precision 38.6%
- among matched: label 100.0%, numeric 8.0%, CI 84.1%, full row 78.4%
- pooled misclassified 0, false extractions 29

## Examples

### hahn-2024-exercise-intake
- missed: Bozinosvki 2009 NW 15min Treadmill 18.00 (p22)
- missed: Bozinosvki 2009 NW 45min Treadmill -23.00 (p22)
- missed: Saunders 2013 NW wallking + PA -89.00 (p22)
- false: Bozinovski 2009 NW 15min Treadmill 18 (p22)
- false: Bozinovski 2009 NW 45min Treadmill -23 (p22)
- false: Miguet 2018 OB 15min HIT 115 (p22)
- false: Saunders 2013 NW walking + PA -89 (p22)
- false: Bozinovski 2009 NW 15min Treadmill 18 (p22)
- false: Bozinovski 2009 NW 45min Treadmill -23 (p22)
- false: Saunders 2013 NW walking + PA -89 (p22)
- false: Bozinovski 2009 NW 15min Treadmill 18 (p23)

### driessen-2015-nih-psychotherapy
- missed: Arean, 2010 0.39 (p13)
- missed: Beutler, 1991 0.09 (p13)
- missed: Hayden, 2012 0.41 (p13)
- missed: O'Hara, 2000 1.14 (p13)
- missed: Spinelli, 2003 0.84 (p13)
- missed: Strachowski, 2008 1.58 (p13)
- missed: Swartz, 2008 0.85 (p13)
- missed: Thompson, 1987 0.41 (p13)
- false: O'Hain, 2000 1.14 (p13)
- false: Stachowski, 2008 1.58 (p13)
- false: Thompson, 1967 0.41 (p13)
- false: These, unpublished -0.51 (p15)

