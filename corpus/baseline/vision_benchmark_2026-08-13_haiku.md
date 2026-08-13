# Vision Benchmark — 2026-08-13_haiku

**BENCHMARK_AGAINST_PREFREEZE_TRUTH** — truth is AI-reconciled,
human-unverified; rerun after researcher sign-off changes any value.

Provider: live · role OVERRIDE(COMPLEX_EXTRACTION_MODEL) → `claude-haiku-4-5-20251001` · prompt v1

Headline metric: FULL_ROW_EXACT_MATCH ('Row asm' below) — label +
effect + CI pair + weight (where truth has one) all correct
simultaneously for a truth study row.

## Per paper

| Paper | Recall | Precision | Label | Numeric | CI pair | FULL ROW | Pooled misclass | False extr | Inappr. resolve | Abstain | Prov. page | Cost | Latency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| yang-2018-sii | 100.0% | 100.0% | 100.0% | 100.0%/100.0% | 100.0% | **100.0%** | 0 | 0 | 0 | 0 | 100.0% | $0.0696 | 66421ms |
| prochaska-2012-varenicline | 97.7% | 95.5% | 100.0% | 100.0%/100.0% | 100.0% | **100.0%** | 2 | 1 | 0 | 0 | 100.0% | $0.0374 | 34937ms |
| hahn-2024-exercise-intake | 51.4% | 90.2% | 100.0% | 0.0%/100.0% | 83.8% | **0.0%** | 0 | 4 | 0 | 0 | 75.7% | $0.2549 | 259670ms |
| driessen-2015-nih-psychotherapy | 27.0% | 77.4% | 100.0% | 37.5%/37.5% | 29.2% | **25.0%** | 0 | 7 | 0 | 2 | 41.7% | $0.1774 | 182601ms |

### By region kind

- yang-2018-sii · RASTER_IMAGE: 2 region(s), 40 rows extracted
- prochaska-2012-varenicline · RASTER_IMAGE: 3 region(s), 45 rows extracted
- hahn-2024-exercise-intake · VECTOR_CLUSTER: 6 region(s), 54 rows extracted
- driessen-2015-nih-psychotherapy · RASTER_IMAGE: 6 region(s), 37 rows extracted

## Aggregate (secondary to per-paper)

- study-row recall 57.6%, precision 91.3%
- among matched: label 100.0%, numeric 62.0%, CI 83.2%, full row 59.9%
- pooled misclassified 2, false extractions 12

## Examples

### prochaska-2012-varenicline
- missed: Tashkin 2011 0.0031 (p11)
- false: Taskhin 2011 0.0031 (p11)

### hahn-2024-exercise-intake
- missed: Ajibewa 2017 NW 25% stretching 17.00 (p22)
- missed: Ajibewa 2017 NW 50% push-ups 73.00 (p22)
- missed: Ajibewa 2017 OB 25% -59.00 (p22)
- missed: Ajibewa 2017 OB 50% 79.00 (p22)
- missed: Bozinosvki 2009 NW 15min Treadmill 18.00 (p22)
- missed: Bozinosvki 2009 NW 45min Treadmill -23.00 (p22)
- missed: Fearnbach 2016 OB 45min cycling 79.00 (p22)
- missed: Nemet 2010 NW 45min resistance training 169.00 (p22)
- false: Bozinovski 2009 NW 15min Treadmill 18 (p22)
- false: Bozinovski 2009 NW 45min Treadmill -23 (p22)
- false: Miguel 2018 OB 15min HIIT 115 (p22)
- false: Saunders 2013 NW walking + PA -89 (p22)

### driessen-2015-nih-psychotherapy
- missed: Arean, 2010 0.39 (p13)
- missed: Dimidjian, 2006 0.25 (p13)
- missed: Hayden, 2012 0.41 (p13)
- missed: O'Hara, 2000 1.14 (p13)
- missed: Rohan, 2007 1.01 (p13)
- missed: Spinelli, 2003 0.84 (p13)
- missed: Strachowski, 2008 1.58 (p13)
- missed: Swartz, 2008 0.85 (p13)
- false: Cox, 1987 1.84 (p14)
- false: Dimidjan, 2006 0.22 (p14)
- false: Mintz, 2001 0.51 (p14)
- false: Unpublished 0.44 (p14)
- false: Unpublished -0.24 (p14)
- false: Dimidjan, 2006 -0.16 (p15)
- false: Rusch, 1977 0.00 (p15)

