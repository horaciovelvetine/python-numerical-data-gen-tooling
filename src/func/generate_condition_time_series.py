def generate_condition_time_series(
    age_in_months: int,
    current_condition_index: int,
    decay_rate: float,
) -> dict:
    """
    Generate a condition time series (historical condition estimates) for an
    asset given its current age (in years) and current condition index. The
    function computes the condition index for each historical year (up to the
    last 10 years or as far back as possible), reversing the effect of
    exponential decay, and records the estimated yearly and monthly condition
    values in a dictionary. The current month's value is set to the actual
    current_condition_index. Returns a dictionary containing keys "year" and
    "months", each mapping to a dictionary of historical condition values.
    """

    R = decay_rate

    condition_history = {"year": {}, "months": {}}

    # Calculate up to last 10 years of historical yearly condition
    # estimates (or as far back as possible)
    max_years = min(10, (age_in_months // 12) + 1)
    for i in range(max_years):
        years_ago = (age_in_months // 12) - i
        months_ago = years_ago * 12
        months_elapsed = age_in_months - months_ago
        # "Undo" the compounded decay for the elapsed months between then and now
        if months_elapsed > 0:
            # Estimate past condition using exponential decay reversal
            condition_past = current_condition_index / ((1 - R) ** months_elapsed)
        else:
            # If months_elapsed is 0 (i.e., "now"), just use the current condition index
            condition_past = current_condition_index
        condition_history["year"][years_ago] = condition_past

    # Calculate monthly condition history for the same period
    # Generate monthly values for up to the last 10 years (120 months) or as far back as possible
    max_months = min(120, age_in_months + 1)
    for i in range(max_months):
        month_ago = age_in_months - i
        months_elapsed = i
        # "Undo" the compounded decay for the elapsed months between then and now
        if months_elapsed > 0:
            # Estimate past condition using exponential decay reversal
            condition_past = current_condition_index / ((1 - R) ** months_elapsed)
        else:
            # If months_elapsed is 0 (i.e., "now"), just use the current condition index
            condition_past = current_condition_index
        condition_history["months"][month_ago] = condition_past

    return condition_history
