from enum import Enum

class TimeSeriesPeriod(Enum):
    """
    TimeSeriesPeriod enumerates the possible intervals for a time series data aggregation.

    Attributes:
      Yearly: Represents yearly time periods (e.g., one data point per year).
      Monthly: Represents monthly time periods (e.g., one data point per month).

    Use this enum to specify the granularity/frequency for time series analyses or reporting.
    """

    Yearly = "Yearly"
    Monthly = "Monthly"
