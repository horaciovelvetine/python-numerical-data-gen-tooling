def calculate_facility_decay_rate(
    age_in_months: int, current_condition_index: int
) -> float:
    """
      Calculate a probable condition decay rate using the provided A = P * (1 - R)^t
    A = current_condition_index (provided)
    P = initial condition (default 99.99)
    R = the condition decay rate
    t = Age (provided in years), converted to months based on the current month

    Re-Arranged:
    R = 1 - (A / P) ** (1 / t)

    Source: "Simulate Data - US Space Template.xlx // 'Facility Condition Index'"
    """
    P = 99.999  # Starting Condition Index
    if age_in_months == 0:
        return 0
    else:
        ratio = current_condition_index / P
        return 1 - ratio ** (1 / age_in_months)
