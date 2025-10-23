"""
Aggregate-based estimator (Eva Pavlik's version).
"""


def ep_estimate_remaining_service_life(agents, facility, age_in_years: int) -> float:
    remaining_months = [a['remaining_months'] for a in agents]
    remaining_months_sorted = sorted(remaining_months)
    mid = len(remaining_months_sorted) // 2
    if len(remaining_months_sorted) % 2 == 1:
        median = remaining_months_sorted[mid]
    else:
        median = 0.5 * (remaining_months_sorted[mid - 1] + remaining_months_sorted[mid])
    return max(0.0, min(facility.life_expectancy - age_in_years, median / 12.0))
