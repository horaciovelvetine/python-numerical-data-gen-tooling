from datetime import datetime
from typing import Dict
from models import ConditionIndex, Facility, TimeSeriesPeriod


class ConditionIndexTimeSeries:
    _period: TimeSeriesPeriod
    _decay_rate: float
    _values: Dict[tuple[int, int], ConditionIndex]

    def __init__(self, period: TimeSeriesPeriod, facility: Facility) -> None:
        self._values = dict()
        self._period = period
        self._decay_rate = self.calculate_probable_decay_rate(facility)
        # Time History Calculation
        if self._period is TimeSeriesPeriod.Monthly:
            self.calculate_monthly_history(facility)
        else:
            self.calculate_yearly_history(facility)

    def calculate_yearly_history(self, facility: Facility):
        """
        Populates self._values with the yearly history of the facility's condition index, up to a maximum of 10 years back.
        The dictionary key is the year (int), and the value is the calculated condition index for that year.
        """

        years_to_calculate = min(10, facility.age + 1)
        current_year = datetime.now().year
        latest_condition = (
            facility.condition_index
        )  # This is the current/latest CI value

        for i in range(years_to_calculate):
            years_ago = years_to_calculate - 1 - i
            t = facility.age - years_ago
            # The farther in the past (i larger), the higher the initial condition index should be,
            # 'reverse' the decay using (1 - r) ** t
            if t < 0:
                continue  # skip invalid negative time
            try:
                # Given A = P * (1 - r)^t, and we know A at current time,
                # Estimate the historical value: Past = Present / (1 - r) ** (years since that past)
                condition = latest_condition / ((1 - self._decay_rate) ** (years_ago))
            except ZeroDivisionError:
                condition = float("inf")
            year_key = current_year - years_ago
            self._values[(year_key, 1)] = ConditionIndex(condition)

    def calculate_monthly_history(self, facility: Facility):
        """
        Calculates monthly condition index history up to 10 years back, populating _values.
        The key is a tuple of (year, month), and the calculation is performed for each month.
        """

        total_months = min(10 * 12, (facility.age + 1) * 12)
        now = datetime.now()
        for i in range(total_months):
            months_ago = (facility.age * 12 + now.month - 1) - i
            year = now.year - (months_ago // 12)
            month = now.month - (months_ago % 12)
            if month <= 0:
                year -= 1
                month += 12

            t = facility.age * 12 - months_ago  # t goes from 0 to total_months-1
            # Adjust decay formula for months (monthly compounding)
            if t < 0:
                continue
            # (1 - r_monthly)**t_months, where r_monthly is the monthly decay rate
            r_monthly = 1 - (1 - self._decay_rate) ** (1 / 12)
            try:
                condition = facility.condition_index / ((1 - r_monthly) ** t)
            except ZeroDivisionError:
                condition = float("inf")
            self._values[(year, month)] = ConditionIndex(condition)

    def calculate_probable_decay_rate(self, facility: Facility) -> float:
        """
        Calculate a probable condition decay rate using the formula:
          A = P * (1 - R)^t

        where:
          A = current_condition_index (provided)
          P = initial condition (default 99.999)
          R = the decay rate to solve for
          t = age (in years or months, depending on period)

        Rearranged:
          R = 1 - (A / P) ** (1 / t)

        - For yearly: t = facility.age (years)
        - For monthly: t = facility.age * 12 + current_month_offset (months)

        Source: "Simulate Data - US Space Template.xlx // 'Facility Condition Index'"
        """

        P = 99.999  # initial condition
        current_index = facility.condition_index

        if self._period == TimeSeriesPeriod.Yearly:
            t = facility.age
            if t == 0:
                return 0
            ratio = current_index / P
            return 1 - ratio ** (1 / t)
        elif self._period == TimeSeriesPeriod.Monthly:
            now = datetime.now()
            years = facility.age
            # t in months is full years + completed months of current year
            t = years * 12 + now.month - 1
            if t == 0:
                return 0
            ratio = current_index / P
            return 1 - ratio ** (1 / t)
        else:
            raise ValueError(f"Unsupported TimeSeriesPeriod: {self._period}")

    @property
    def period(self) -> TimeSeriesPeriod:
        return self._period

    @property
    def decay_rate(self) -> float:
        return self._decay_rate

    @property
    def history(self) -> Dict[tuple(int, int), ConditionIndex]:
        return self._values
