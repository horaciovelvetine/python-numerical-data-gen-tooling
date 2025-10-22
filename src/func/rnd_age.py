import random


def rnd_age(facility_life_expectancy):
    """
    Generates a random age value, given a FacilityLifeExpectancy.
    The distribution matches README.md recommendations:
      - 50%: 20–40 years
      - 20%: 10–20 years
      - 20%: 41 years up to life expectancy
      - 10%: less than 10 years

    Args:
        facility_life_expectancy (FacilityLifeExpectancy): Enum value with
            a .life_expectancy attribute

    Raises:
        ValueError: if facility_life_expectancy.life_expectancy < 10
    """
    LE = facility_life_expectancy.life_expectancy

    if LE < 10:
        raise ValueError("Life expectancy of facility must be at least 10 years")

    # Distribution bins and their weights
    buckets = [
        (10, 0, min(9, LE)),  # 10%: [0, 9] (less than 10 years)
        (20, 10, min(20, LE)),  # 20%: [10, 20]
        (50, 20, min(40, LE)),  # 50%: [20, 40]
        (20, max(41, 0), LE),  # 20%: [41, LE]
    ]

    # Adjust buckets dynamically based on max life expectancy
    ranges = []
    weights = []
    for weight, start, end in buckets:
        # Only build ranges that have valid domain
        if end < start:
            continue
        ranges.append((start, end))
        weights.append(weight)

    # Normalize weights (may add up to less than 100 if high LE is < 41)
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]

    # Choose a bucket by weighted random selection
    chosen_range = random.choices(ranges, weights=weights, k=1)[0]
    # Uniformly pick a year in the selected bucket (inclusive)
    return random.randint(chosen_range[0], chosen_range[1])
