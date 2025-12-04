from datetime import datetime

# Models From self.Library
from models import ConditionIndex, ConditionIndexTimeSeries, Dependency, ResiliencyGrade, TimeSeriesPeriod, FacilityType


class Facility:
    MAXIMUM_AGE = 80

    # ? Attributes in order of "Facility Condition Index" tab from "Simulate Data" spreadsheet
    _site: str
    _installation: str
    _mission_criticality: int  # value between 1-3
    _facility_number: int
    _year_constructed: int
    # _age value computed
    # _state_degraded computed
    # _state_degraded_realized random occurrence off of simulation
    _facility_type: FacilityType  # for title, key, tier, and life_expectancy
    _dependency_chain: Dependency
    _resiliency_grade: ResiliencyGrade
    _condition_index: ConditionIndex
    # _condition_index_time_series computed value
    _unique_identifier: int

    # * GETTERS AND SETTERS / GETTERS AND SETTERS / GETTERS AND SETTERS
    # * GETTERS AND SETTERS / GETTERS AND SETTERS / GETTERS AND SETTERS
    # * GETTERS AND SETTERS / GETTERS AND SETTERS / GETTERS AND SETTERS

    @property
    def site(self) -> str:
        return self._site

    @site.setter
    def site(self, site_name: str):
        if site_name.strip() == "":
            raise ValueError("Site value provided cannot be empty or only spaces")
        self._site = site_name

    @property
    def installation(self) -> str:
        return self._installation

    @installation.setter
    def installation(self, installation_name: str):
        if installation_name.strip() == "":
            raise ValueError(
                "Installation value provided cannot be empty or only spaces"
            )
        self._installation = installation_name

    @property
    def facility_number(self) -> int:
        return self._facility_number

    @facility_number.setter
    def facility_number(self, n: int):
        if n <= 0:
            raise ValueError("Facility Number value provided cannot be 0 or negative")
        self._facility_number = n

    # * TITLE / KEY / TIER / LIFE_EXPECTANCY / TITLE / KEY / TIER / LIFE_EXPECTANCY
    # * TITLE / KEY / TIER / LIFE_EXPECTANCY / TITLE / KEY / TIER / LIFE_EXPECTANCY
    # * TITLE / KEY / TIER / LIFE_EXPECTANCY / TITLE / KEY / TIER / LIFE_EXPECTANCY

    @property
    def title(self) -> str:
        return self._facility_type.title

    @property
    def key(self) -> int:
        return self._facility_type.key

    @property
    def life_expectancy(self) -> int:
        return self._facility_type.life_expectancy

    @property
    def facility_tier(self) -> str:
        #TODO --> Implementation Details
        return self._facility_type.tier

    # @title.setter
    # def title(self, t: str):
    #     if t.strip() == "":
    #         raise ValueError("Title value provided cannot be empty or only spaces")
    #     self._title = t

    # ? NUMERICAL GETTERS & SETTERS
    # ? NUMERICAL GETTERS & SETTERS
    # ? NUMERICAL GETTERS & SETTERS

    @property
    def age(self) -> int:
        return datetime.now().year - self._year_constructed

    @property
    def year_constructed(self) -> int:
        return self._year_constructed

    @year_constructed.setter
    def year_constructed(self, y: int):
        current_year = datetime.now().year
        construction_year_max = current_year - self.MAXIMUM_AGE
        if y > current_year:
            raise ValueError(
                f"Year Constructed cannot be greater than the current year given: {y}"
            )
        elif y < 0:
            raise ValueError("Year Constructed cannot be less than 0")
        elif y < construction_year_max:
            raise ValueError(
                f"Year Constructed cannot be more than: {self.MAXIMUM_AGE} years ago, per documentation"
            )

        self._year_constructed = y

    @property
    def condition_index(self) -> float:
        return self._condition_index.value

    @condition_index.setter
    def condition_index(self, ind: float = None):
        self._condition_index = ConditionIndex(ind)

    @property
    def state_degraded(self) -> bool:
        return self._condition_index.is_degraded()

    @property
    def resiliency_grade(self) -> ResiliencyGrade:
        return self._resiliency_grade

    @resiliency_grade.setter
    def resiliency_grade(self, grade_number: int):
        if grade_number < 1 or grade_number > 4:
            raise ValueError(
                f"Invalid Resiliency Grade value provided: {grade_number}. Must be an integer between 1 and 4."
            )
        if grade_number == 1:
            self._resiliency_grade = ResiliencyGrade.G1
        elif grade_number == 2:
            self._resiliency_grade = ResiliencyGrade.G2
        elif grade_number == 3:
            self._resiliency_grade = ResiliencyGrade.G3
        else:
            self._resiliency_grade = ResiliencyGrade.G4

    @property
    def condition_index_time_series(
        self, period: TimeSeriesPeriod
    ) -> ConditionIndexTimeSeries:
        return ConditionIndexTimeSeries(period, self)
