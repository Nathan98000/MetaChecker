import os
import time
import uuid

_last: tuple[int, int] = (0, 0)


def uuid7() -> str:
    """UUIDv7 (RFC 9562): 48-bit unix-ms timestamp + random, time-sortable.

    Python 3.12's stdlib lacks uuid7; this implementation keeps ordering
    monotonic within the process for ids minted in the same millisecond.
    """
    global _last
    ms = time.time_ns() // 1_000_000
    seq = 0
    if ms <= _last[0]:
        ms, seq = _last[0], _last[1] + 1
    _last = (ms, seq)

    rand_a = seq & 0x0FFF  # 12-bit monotonic counter within the millisecond
    rand_b = int.from_bytes(os.urandom(8), "big") & ((1 << 62) - 1)
    value = (
        (ms & ((1 << 48) - 1)) << 80
        | 0x7 << 76
        | rand_a << 64
        | 0b10 << 62
        | rand_b
    )
    return str(uuid.UUID(int=value))
