"""SQLite concurrency measurement (doc 00 O4: measure, don't assume).

Simulates the real write pattern: one worker thread committing short write
transactions while API-like readers query concurrently under WAL. Reports
measurements; fails only on actual errors or pathological latency.
"""

import statistics
import threading
import time

from sqlalchemy import select

from app.db.models import Project, StageState


def test_concurrent_reads_during_writes_under_wal(session_factory, project):
    write_latencies: list[float] = []
    read_latencies: list[float] = []
    errors: list[str] = []
    N_WRITES = 200
    N_READERS = 4

    def writer():
        for i in range(N_WRITES):
            t0 = time.perf_counter()
            try:
                with session_factory() as s:
                    s.add(
                        StageState(
                            project_id=project.id,
                            stage_id="bench",
                            work_item_ref=f"item-{i}",
                            state="SUCCESS",
                        )
                    )
                    s.commit()
            except Exception as exc:  # noqa: BLE001
                errors.append(f"write: {exc}")
            write_latencies.append(time.perf_counter() - t0)

    def reader(stop: threading.Event):
        while not stop.is_set():
            t0 = time.perf_counter()
            try:
                with session_factory() as s:
                    s.scalars(select(Project)).all()
                    s.scalars(select(StageState).limit(50)).all()
            except Exception as exc:  # noqa: BLE001
                errors.append(f"read: {exc}")
            read_latencies.append(time.perf_counter() - t0)

    stop = threading.Event()
    readers = [threading.Thread(target=reader, args=(stop,)) for _ in range(N_READERS)]
    for r in readers:
        r.start()
    w = threading.Thread(target=writer)
    w.start()
    w.join()
    stop.set()
    for r in readers:
        r.join()

    p95_write = statistics.quantiles(write_latencies, n=20)[18]
    p95_read = statistics.quantiles(read_latencies, n=20)[18]
    throughput = N_WRITES / sum(write_latencies)
    print(
        f"\nSQLite WAL measurements: writes={N_WRITES} readers={N_READERS} | "
        f"write p50={statistics.median(write_latencies)*1e3:.2f}ms "
        f"p95={p95_write*1e3:.2f}ms | read p50={statistics.median(read_latencies)*1e3:.2f}ms "
        f"p95={p95_read*1e3:.2f}ms | write throughput≈{throughput:.0f}/s"
    )

    assert not errors, errors[:5]
    # Generous bound: this flags real contention pathology, not normal variance.
    assert p95_write < 0.5, f"p95 write latency {p95_write:.3f}s suggests contention"
