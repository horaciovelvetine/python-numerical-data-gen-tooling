from const.facility_life_expectancy import FacilityLifeExpectancy


class Facility:
    """
    Represents a facility asset instance with metadata and computed properties.

    Attributes:
        title (str): The title/name of the facility type.
        expected_service_life (int): The expected service life (years) of
            the facility type.
        facility_key (str): The unique key/identifier for the facility
            type.
        age_in_years (int): The current age of the facility in years.
        condition_index (float): The current condition index of the
            facility asset.
        time_series (dict): A time series containing historical and current
            condition indices (typically by year/month).
        estimated_remaining_service_life (float): The estimated remaining
            service life in years.

    Args:
        facility (FacilityLifeExpectancy): Facility life expectancy
            definition object.
        age_in_years (int): Current age of the facility asset (in years).
        condition_index (float): The facility's current condition index.
        time_series (dict): Time series of (historical/current) condition
            indices.
        estimated_remaining_service_life (float): Estimated remaining
            service life in years.
    """

    def __init__(
        self,
        facility: FacilityLifeExpectancy,
        age_in_years: int,
        condition_index: float,
        time_series: dict,
        estimated_remaining_service_life: float,
    ):
        self.title = facility.title
        self.expected_service_life = facility.life_expectancy
        self.facility_key = facility.key
        self.age_in_years = age_in_years
        self.condition_index = condition_index
        self.time_series = time_series
        self.estimated_remaining_service_life = estimated_remaining_service_life

    def to_dict(self):
        """
        Convert the Facility object to a dictionary for serialization.

        Returns:
            dict: A dictionary containing all properties of the object.
        """
        return {
            "title": self.title,
            "expected_service_life": self.expected_service_life,
            "facility_key": self.facility_key,
            "age_in_years": self.age_in_years,
            "condition_index": self.condition_index,
            "time_series": self.time_series,
            "estimated_remaining_service_life": self.estimated_remaining_service_life,
        }
