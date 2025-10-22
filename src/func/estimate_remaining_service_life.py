import math
from const.facility_life_expectancy import FacilityLifeExpectancy


def estimate_remaining_service_life(
    decay_rate: float, age_in_years: int, facility: FacilityLifeExpectancy
) -> float:
    """
    Estimate the remaining service life of a facility based on its current
    decay rate, age, and definition.

    Args:
        decay_rate (float): Estimated annual decay rate.
        age_in_years (int): Current age of the facility in years.
        facility (FacilityLifeExpectancy): Facility definition object
            containing life_expectancy.
    """
    DEGRADED_THRESHOLD = 25.0  # FCI threshold for end-of-life
    P = 99.999  # Initial "Condition Index"

    # If decay_rate <=0, assume no decay, return max service life
    if decay_rate <= 0:
        # If the asset is older than "expected", still cap at 0
        return max(0, facility.life_expectancy - age_in_years)
    elif decay_rate >= 1:
        # With such a high decay the asset is at or past critical
        # threshold
        raise RuntimeError(
            "Facilty decay_rate calculated above 1, unable to estimate "
            "remaining service life"
        )

    try:
        # Calculate the total age (years) when the asset will hit DEGRADED_THRESHOLD
        # Solve for t: threshold = P * (1 - R)^t  =>  t = log(threshold/P) / log(1-R)
        total_age_at_threshold = math.log(DEGRADED_THRESHOLD / P) / math.log(
            1 - decay_rate
        )
        remaining_life = total_age_at_threshold - age_in_years
        # Remaining life cannot exceed the max life expectancy nor be below 0
        max_remaining = facility.life_expectancy - age_in_years
        return max(0, min(remaining_life, max_remaining))
    except (ValueError, ZeroDivisionError):
        # If there's any math error return 0
        raise RuntimeError(
            "Unable to estimate remaining service life due to math error."
        )
