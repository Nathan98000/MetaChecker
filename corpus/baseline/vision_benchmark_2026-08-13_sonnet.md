# Vision Benchmark — 2026-08-13_sonnet

**BENCHMARK_AGAINST_PREFREEZE_TRUTH** — truth is AI-reconciled,
human-unverified; rerun after researcher sign-off changes any value.

Provider: live · role OVERRIDE(COMPLEX_EXTRACTION_MODEL) → `claude-sonnet-5` · prompt v1

Headline metric: FULL_ROW_EXACT_MATCH ('Row asm' below) — label +
effect + CI pair + weight (where truth has one) all correct
simultaneously for a truth study row.

## Per paper

| Paper | Recall | Precision | Label | Numeric | CI pair | FULL ROW | Pooled misclass | False extr | Inappr. resolve | Abstain | Prov. page | Cost | Latency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| yang-2018-sii | 100.0% | 60.7% | 100.0% | 100.0% | 100.0% | **100.0%** | 0 | 22 | 0 | 33 | 100.0% | $0.1554 | 97305ms |
| prochaska-2012-varenicline | 100.0% | 97.7% | 100.0% | 100.0% | 100.0% | **100.0%** | 2 | 0 | 0 | 0 | 100.0% | $0.1374 | 60146ms |
| hahn-2024-exercise-intake | 19.4% | 100.0% | 100.0% | 0.0% | 57.1% | **0.0%** | 0 | 0 | 0 | 0 | 0.0% | $0.8754 | 402193ms |
| driessen-2015-nih-psychotherapy | 49.4% | 91.7% | 100.0% | 0.0% | 0.0% | **0.0%** | 0 | 4 | 0 | 4 | 54.5% | $0.577 | 251249ms |

### By region kind

- yang-2018-sii · RASTER_IMAGE: 6 region(s), 72 rows extracted
- prochaska-2012-varenicline · RASTER_IMAGE: 3 region(s), 48 rows extracted
- hahn-2024-exercise-intake · VECTOR_CLUSTER: 10 region(s), 52 rows extracted
- driessen-2015-nih-psychotherapy · RASTER_IMAGE: 7 region(s), 70 rows extracted

## Aggregate (secondary to per-paper)

- study-row recall 56.7%, precision 83.3%
- among matched: label 100.0%, numeric 57.0%, CI 63.0%, full row 57.0%
- pooled misclassified 2, false extractions 26

## Examples

### yang-2018-sii
- false: Hong UNRESOLVED (p5)
- false: Loll UNRESOLVED (p5)
- false: Passardi UNRESOLVED (p5)
- false: Liu UNRESOLVED (p5)
- false: wang UNRESOLVED (p5)
- false: Tong UNRESOLVED (p5)
- false: Jin UNRESOLVED (p5)
- false: Yu UNRESOLVED (p5)

### hahn-2024-exercise-intake
- missed: Ajibewa 2017 NW 25% stretching 17.00 (p22)
- missed: Ajibewa 2017 NW 50% push-ups 73.00 (p22)
- missed: Ajibewa 2017 OB 25% -59.00 (p22)
- missed: Ajibewa 2017 OB 50% 79.00 (p22)
- missed: Bozinosvki 2009 NW 15min Treadmill 18.00 (p22)
- missed: Bozinosvki 2009 NW 45min Treadmill -23.00 (p22)
- missed: Fearnbach 2016 OB 45min cycling 79.00 (p22)
- missed: Fearnbach Silvert 2017 NW 45min cycling 110.00 (p22)

### driessen-2015-nih-psychotherapy
- missed: [unnamed unpublished] 0.31 (p13)
- missed: O'Hara, 2000 1.14 (p13)
- missed: Rohan, 2007 1.01 (p13)
- missed: Strachowski, 2008 1.58 (p13)
- missed: Blum, unpublished 0.50 (p13)
- missed: Arean, 2010 0.39 (p14)
- missed: Barber, 2012 0.08 (p14)
- missed: DeRubeis, 2005 0.45 (p14)
- false: Blank 0,31 (p14)
- false: Unpublished 0,44 (p14)
- false: Unpublished -0,24 (p14)
- false: Blank 0,56 (p15)

