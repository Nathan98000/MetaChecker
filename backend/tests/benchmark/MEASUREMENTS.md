# Database Measurements Log

Per doc 00 O4: SQLite is reconsidered only on measured limitations, and
measurements are recorded before any database change.

## 2026-08-11 — Foundation baseline (SQLite WAL)

Machine: development Mac (Apple Silicon), macOS, SQLite via SQLAlchemy 2.
Workload: 200 sequential short write transactions (worker pattern) with 4
concurrent reader threads (API pattern), WAL mode, busy_timeout 30s.

```text
write p50 = 0.29 ms    write p95 = 0.78 ms
read  p50 = 2.47 ms    read  p95 = 5.15 ms
write throughput ≈ 2,656 tx/s
errors: 0 (no SQLITE_BUSY surfaced)
```

Interpretation: orders of magnitude above the pipeline's write needs (a full
parse commits a handful of transactions per document). No inadequacy trigger
approached. Re-run via `pytest tests/benchmark -s` and append results here
whenever the write pattern changes materially.
