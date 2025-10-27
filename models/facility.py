"""
Facility model for representing facility data and metadata.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Facility:
    """
    Represents a facility with its properties and simulation results.
    """
    
    facility: Any  # FacilityLifeExpectancy enum
    age_in_years: float
    condition_index: float
    time_series: Dict[str, Any]
    estimated_remaining_service_life: float
    
    @property
    def title(self) -> str:
        """Get the facility title."""
        return self.facility.title
    
    @property
    def expected_service_life(self) -> int:
        """Get the expected service life."""
        return self.facility.life_expectancy
    
    @property
    def key(self) -> int:
        """Get the facility key."""
        return self.facility.key
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the facility to a dictionary representation.
        
        Returns:
            Dictionary containing all facility data
        """
        return {
            "facility": {
                "key": self.key,
                "title": self.title,
                "life_expectancy": self.expected_service_life
            },
            "age_in_years": self.age_in_years,
            "condition_index": self.condition_index,
            "time_series": self.time_series,
            "estimated_remaining_service_life": self.estimated_remaining_service_life,
            "expected_service_life": self.expected_service_life
        }
    
    def __str__(self) -> str:
        """String representation of the facility."""
        return (f"Facility(title='{self.title}', "
                f"age={self.age_in_years:.1f}y, "
                f"condition={self.condition_index:.3f}, "
                f"rsl={self.estimated_remaining_service_life:.1f}y)")
    
    def __repr__(self) -> str:
        """Detailed representation of the facility."""
        return self.__str__()