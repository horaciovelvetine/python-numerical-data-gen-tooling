from datetime import datetime


def get_age_in_months(current_age: int) -> int:
    """
    Converts the given age in years to age in months, accounting for the
    months elapsed in the current year up to the present month.

    Args:
        current_age (int): The age of the asset in years.
    """
    now = datetime.now()
    age = (current_age * 12) + (now.month - 1)
    return age
