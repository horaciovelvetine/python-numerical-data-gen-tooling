import random


def rnd_condition_index() -> int:
    """
    Returns a random condition index in the range 1-99, following this distribution:
        - 7% below 50 (i.e., 1-49)
        - 5% above 85 (i.e., 86-99)
        - Remainder (88%) between 50-85 (inclusive)
    The mean value is ~70.
    """
    # Define the buckets and their weights
    buckets = [
        (1, 49, 0.07),  # 7%: 1-49
        (50, 85, 0.88),  # 88%: 50-85
        (86, 99, 0.05),  # 5%: 86-99
    ]

    # Prepare ranges and weights
    ranges = [(b[0], b[1]) for b in buckets]
    weights = [b[2] for b in buckets]

    # Select range by weighted random choice
    chosen_range = random.choices(ranges, weights=weights, k=1)[0]

    # Select integer in chosen range, inclusive
    return random.randint(chosen_range[0], chosen_range[1])
