from enum import Enum


class FacilityLifeExpectancy(Enum):
    """Enumeration of facility types with their expected life expectancy."""
    
    HEATING_COOLING_PLANT = (1, "Heating - Cooling Plant", 60)
    ANTENNA_SUPPORT_BUILDING = (2, "Antenna support building", 30)
    COMMUNICATION_FACILITY = (3, "Communication Facility", 60)
    POWER_GENERATION_FACILITY = (4, "Power generation Facility", 60)
    GROUND_TERMINAL_T1 = (5, "Ground Terminal T1", 30)
    OPS_FACILITY_T1 = (6, "Ops Facility T1", 50)
    DATA_CENTER = (7, "Data Center", 40)
    RECEIVER_STATION = (8, "Receiver Station", 30)
    GROUND_MONITORING_STATION = (9, "Ground monitoring Station", 30)
    PUMP_STATION = (10, "Pump Station", 40)
    ADMIN_OFFICE = (11, "Admin Office", 40)
    EQUIPMENT_PAD = (12, "Equipment Pad", 20)
    FUEL_BUILDING = (13, "Fuel Building", 50)
    DORM_FACILITY = (14, "Dorm Facility", 50)
    CENTRAL_UTILITY_PLANT = (15, "Central Utility Plant", 50)
    TRUCK_FILL_STAND = (16, "Truck fill stand", 30)
    ENTRY_CONTROL_POINT = (17, "Entry control point", 30)
    UTILITY_CORRIDOR = (18, "Utility corridor", 60)
    MAINTENANCE_SHOP = (19, "Maintenance Shop", 40)
    FUEL_FARM = (20, "Fuel Farm", 40)
    RADOME_FACILITY = (21, "Radome Facility", 30)
    WATER_TREATMENT_FACILITY = (22, "Water Treatment Facility", 30)
    STANDBY_GENERATOR = (23, "Standby Generator", 30)
    UPS_BUILDING = (24, "UPS Building", 50)
    SWITCHING_STATION = (25, "Switching Station", 30)
    SUBSTATION = (26, "Substation", 30)
    FUEL_INTAKE_FACILITY = (27, "Fuel intake Facility", 30)
    STORAGE_FACILITY = (28, "Storage Facility", 60)
    
    def __init__(self, key: int, title: str, life_expectancy: int):
        self.key = key
        self.title = title
        self.life_expectancy = life_expectancy
    
    @classmethod
    def is_valid_title(cls, title: str) -> bool:
        """Check if a title is valid."""
        return any(facility.title == title for facility in cls)
    
    @classmethod
    def find_by_title(cls, title: str):
        """Find facility by title."""
        for facility in cls:
            if facility.title == title:
                return facility
        raise ValueError(f"No facility found with title: {title}")
    
    @classmethod
    def get_all_titles(cls) -> list:
        """Get all facility titles."""
        return [facility.title for facility in cls]


facility_life_expectancy_data = [
    {"key": 1, "label": "Heating - Cooling Plant", "life_expectancy": 60},
    {"key": 2, "label": "Antenna support building", "life_expectancy": 30},
    {"key": 3, "label": "Communication Facility", "life_expectancy": 60},
    {"key": 4, "label": "Power generation Facility", "life_expectancy": 60},
    {"key": 5, "label": "Ground Terminal T1", "life_expectancy": 30},
    {"key": 6, "label": "Ops Facility T1", "life_expectancy": 50},
    {"key": 7, "label": "Data Center", "life_expectancy": 40},
    {"key": 8, "label": "Receiver Station", "life_expectancy": 30},
    {"key": 9, "label": "Ground monitoring Station", "life_expectancy": 30},
    {"key": 10, "label": "Pump Station", "life_expectancy": 40},
    {"key": 11, "label": "Admin Office", "life_expectancy": 40},
    {"key": 12, "label": "Equipment Pad", "life_expectancy": 20},
    {"key": 13, "label": "Fuel Building", "life_expectancy": 50},
    {"key": 14, "label": "Dorm Facility", "life_expectancy": 50},
    {"key": 15, "label": "Central Utility Plant", "life_expectancy": 50},
    {"key": 16, "label": "Truck fill stand", "life_expectancy": 30},
    {"key": 17, "label": "Entry control point", "life_expectancy": 30},
    {"key": 18, "label": "Utility corridor", "life_expectancy": 60},
    {"key": 19, "label": "Maintenance Shop", "life_expectancy": 40},
    {"key": 20, "label": "Fuel Farm", "life_expectancy": 40},
    {"key": 21, "label": "Radome Facility", "life_expectancy": 30},
    {"key": 22, "label": "Water Treatment Facility", "life_expectancy": 30},
    {"key": 23, "label": "Standby Generator", "life_expectancy": 30},
    {"key": 24, "label": "UPS Building", "life_expectancy": 50},
    {"key": 25, "label": "Switching Station", "life_expectancy": 30},
    {"key": 26, "label": "Substation", "life_expectancy": 30},
    {"key": 27, "label": "Fuel intake Facility", "life_expectancy": 30},
    {"key": 28, "label": "Storage Facility", "life_expectancy": 60},
]
