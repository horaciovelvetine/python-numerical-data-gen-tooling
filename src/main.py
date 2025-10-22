# Constants
from const.facility_life_expectancy import FacilityLifeExpectancy
from models.facility import Facility

# Functions
from func.rnd_age import rnd_age
from func.get_age_in_months import get_age_in_months
from func.rnd_condition_index import rnd_condition_index
from func.calculate_facility_decay_rate import calculate_facility_decay_rate
from func.generate_condition_time_series import generate_condition_time_series
from func.estimate_remaining_service_life import estimate_remaining_service_life


def get_random_facility_data_nums(facility_title: str) -> Facility:
    """
    Generates random values for all (defined) numerical fields for the
    provided facility type
    """

    if FacilityLifeExpectancy.is_valid_title(facility_title) is not True:
        raise ValueError(f"Unexpected facility title: '{facility_title}'")

    facility = FacilityLifeExpectancy.find_by_title(facility_title)
    age_in_years = rnd_age(facility)
    age_in_months = get_age_in_months(age_in_years)
    condition_index = rnd_condition_index()
    decay_rate = calculate_facility_decay_rate(age_in_months, condition_index)
    time_series = generate_condition_time_series(
        age_in_months, condition_index, decay_rate
    )
    estimated_remaining_service_life = estimate_remaining_service_life(
        decay_rate, age_in_years, facility
    )

    return Facility(
        facility=facility,
        age_in_years=age_in_years,
        condition_index=condition_index,
        time_series=time_series,
        estimated_remaining_service_life=estimated_remaining_service_life,
    )
