from enum import Enum

class FacilityType(Enum):
    """
    FacilityLifeExpectancy is an enumeration of different facility types,
    each with an associated life expectancy in years.

    Source: "Simulate Data - US Space Template.xlx // 'Key'"

    Attributes:
        key (int): A unique integer identifier for the facility type.
        title (str): The human-readable name of the facility.
        life_expectancy (int): The expected useful life span of the facility, in years.
    """

    HEATING_COOLING_PLANT = (1, "Heating - Cooling Plant", 60)
    ANTENNA_SUPPORT_BUILDING = (2, "Antenna support building", 30)
    COMMUNICATION_FACILITY = (3, "Communication Facility", 60)
    POWER_GENERATION_FACILITY = (4, "Power generation Facility", 60)
    GROUND_TERMINAL = (5, "Ground Terminal", 30)
    OPS_FACILITY = (6, "Ops Facility", 50)
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
        self._key = key
        self._title = title
        self._life_expectancy = life_expectancy

    @classmethod
    def get_by_title(t: str) -> "FacilityType":
        pass

    @property
    def key(self) -> int:
        return self._key

    @property
    def title(self) -> str:
        return self._title

    @property
    def tier(self) -> str:
        return self._tier

    @property
    def life_expectancy(self) -> int:
        return self._life_expectancy
