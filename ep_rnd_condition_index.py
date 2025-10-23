"""
Initial condition index sampler for ep_ Monte Carlo (Eva Pavlik's version).
"""
import random


def ep_rnd_condition_index(seed: int | None = None) -> float:
    if seed is not None:
        random.seed(seed + 2)

    buckets = [
        (0.07, 1, 49),
        (0.88, 50, 85),
        (0.05, 86, 99),
    ]
    weights = [b[0] for b in buckets]
    chosen = random.choices(buckets, weights=weights, k=1)[0]
    _, lo, hi = chosen
    base = random.randint(lo, hi)
    jitter = random.uniform(-0.5, 0.5)
    return round(max(1.0, min(99.0, base + jitter)), 2)
