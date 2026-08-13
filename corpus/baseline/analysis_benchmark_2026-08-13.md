# Analysis-Identification Benchmark — 2026-08-13

**BENCHMARK_AGAINST_PREFREEZE_TRUTH** · deterministic structural
identifier v1 (tables + RevMan headers + figure summary rows; vision
channel via recorded fixtures). Text-borne analyses (prose-only pooled
values) are a separate bucket — out of the structural channel's scope,
never silently claimed.

| Paper | Struct. truth | Recall | Precision | I² ok | Measure | Model | k agrees | Extra (unverif.) | Text-only (o.o.s.) |
|---|---|---|---|---|---|---|---|---|---|
| yang-2018-sii | 19 | 89% | 100% | 21% | 100% | 0% | 100% | 0 | 0 |
| prochaska-2012-varenicline | 5 | 100% | 100% | 0% | 40% | 0% | 40% | 0 | 5 |
| macnamara-2014-practice | 2 | 0% | — | — | — | — | — | 0 | 19 |
| hahn-2024-exercise-intake | 13 | 100% | 100% | 0% | 100% | 100% | 100% | 0 | 1 |
| driessen-2015-nih-psychotherapy | 18 | 100% | 100% | 0% | 100% | 0% | 44% | 0 | 13 |
| cooney-2013-exercise-depression | 3 | 100% | 14% | 0% | 100% | 0% | 100% | 19 | 4 |
| nissen-2007-rosiglitazone | 16 | 50% | 100% | — | 100% | 0% | 0% | 0 | 1 |

## Missed / false examples

### yang-2018-sii
- missed: A18 OS 1.21[1.00,1.43]
- missed: A19 OS 1.32[1.14,1.51]

### macnamara-2014-practice
- missed: MAC-OV-2014 Overall practice-performance .35[.30,.39]
- missed: MAC-OV-2018 Overall practice-performance .38[.33,.42]

### cooney-2013-exercise-depression
- extra: Comparison 1 Exercise versus 'control', Outcome 4  0.45[0.06,0.83]
- extra: Comparison 2 Exercise versus psychological therapi -0.03[-0.32,0.26]
- extra: Comparison 2 Exercise versus psychological therapi 1.08[0.95,1.24]
- extra: Comparison 3 Exercise versus bright light therapy, -6.4[-10.2,-2.6]
- extra: Comparison 4 Exercise versus pharmacological treat -0.11[-0.34,0.12]

### nissen-2007-rosiglitazone
- missed: A09 myocardial infarction 1.14[0.70,1.86]
- missed: A10 myocardial infarction 1.24[0.78,1.98]
- missed: A11 myocardial infarction 2.78[0.58,13.3]
- missed: A12 myocardial infarction 1.80[0.95,3.39]
- missed: A13 death from cardiovascular causes 1.13[0.34,3.71]
- missed: A14 death from cardiovascular causes 1.42[0.60,3.33]

