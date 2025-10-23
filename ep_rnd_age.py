"""
Simple age sampler for the ep_ Monte Carlo implementation (Eva Pavlik's version).
"""
import random


def ep_rnd_age(facility_life_expectancy, seed: int | None = None) -> int:
    if seed is not None:
        random.seed(seed + 1)

    LE = facility_life_expectancy.life_expectancy
    buckets = [
        (0.10, 0, min(9, LE)),
        (0.20, 10, min(20, LE)),
        (0.50, 20, min(40, LE)),
        (0.20, 41, LE),
    ]

    valid = [b for b in buckets if b[2] >= b[1]]
    weights = [b[0] for b in valid]
    total = sum(weights)
    weights = [w / total for w in weights]

    chosen = random.choices(valid, weights=weights, k=1)[0]
    _, start, end = chosen
    age = random.randint(start, end)

    age = min(age, LE)
    return age
