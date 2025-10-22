from enum import Enum
from src.const.facility_life_expectancy import FacilityLifeExpectancy


class SystemLifeExpectancy(Enum):
    """
    SystemLifeExpectancy is an enumeration of building system types, each
    with an associated life expectancy (in years) and a set of facility
    types to which the system applies.

    Source: "Simulate Data - US Space Template.xlx // 'Key'"

    Attributes:
        label (str): The name of the building system.
        life_expectancy (int): The expected useful life span of the
            building system, in years.
        facilities (list): A list of FacilityLifeExpectancy enum members
            to which the system applies.
    """

    FOUNDATION = (
        "Foundation",
        60,
        list(FacilityLifeExpectancy),
    )
    BASEMENT = (
        "Basement",
        60,
        [
            FacilityLifeExpectancy.HEATING_COOLING_PLANT,
            FacilityLifeExpectancy.ANTENNA_SUPPORT_BUILDING,
            FacilityLifeExpectancy.COMMUNICATION_FACILITY,
            FacilityLifeExpectancy.POWER_GENERATION_FACILITY,
            FacilityLifeExpectancy.GROUND_TERMINAL_T1,
            FacilityLifeExpectancy.OPS_FACILITY_T1,
            FacilityLifeExpectancy.DATA_CENTER,
            FacilityLifeExpectancy.RECEIVER_STATION,
            FacilityLifeExpectancy.DORM_FACILITY,
            FacilityLifeExpectancy.CENTRAL_UTILITY_PLANT,
            FacilityLifeExpectancy.UTILITY_CORRIDOR,
            FacilityLifeExpectancy.RADOME_FACILITY,
            FacilityLifeExpectancy.UPS_BUILDING,
            FacilityLifeExpectancy.SWITCHING_STATION,
            FacilityLifeExpectancy.SUBSTATION,
        ],
    )
    SUPERSTRUCTURE = ("Superstructure", 50, list(FacilityLifeExpectancy))
    EXTERIOR_STRUCTURE = ("Exterior Structure", 40, list(FacilityLifeExpectancy))
    ROOFING = ("Roofing", 20, list(FacilityLifeExpectancy))
    INTERIOR_CONSTRUCTION = (
        "Interior Construction",
        30,
        [
            f
            for f in FacilityLifeExpectancy
            if f
            not in [
                FacilityLifeExpectancy.TRUCK_FILL_STAND,
                FacilityLifeExpectancy.FUEL_FARM,
                FacilityLifeExpectancy.FUEL_INTAKE_FACILITY,
            ]
        ],
    )
    STAIRS = (
        "Stairs",
        40,
        [
            f
            for f in FacilityLifeExpectancy
            if f
            not in [
                FacilityLifeExpectancy.TRUCK_FILL_STAND,
                FacilityLifeExpectancy.ENTRY_CONTROL_POINT,
                FacilityLifeExpectancy.FUEL_FARM,
                FacilityLifeExpectancy.STANDBY_GENERATOR,
                FacilityLifeExpectancy.FUEL_INTAKE_FACILITY,
            ]
        ],
    )
    INTERIOR_FINISHES = ("Interior Finishes", 20, [])
    CONVEYING = ("Conveying", 10, [])
    PLUMBING = ("Plumbing", 30, [])
    ART = (
        "Art",
        10,
        [
            FacilityLifeExpectancy.OPS_FACILITY_T1,
            FacilityLifeExpectancy.ADMIN_OFFICE,
            FacilityLifeExpectancy.DORM_FACILITY,
            FacilityLifeExpectancy.MAINTENANCE_SHOP,
        ],
    )
    HVAC = (
        "HVAC",
        40,
        [
            f
            for f in FacilityLifeExpectancy
            if f
            not in [
                FacilityLifeExpectancy.EQUIPMENT_PAD,
                FacilityLifeExpectancy.TRUCK_FILL_STAND,
                FacilityLifeExpectancy.ENTRY_CONTROL_POINT,
                FacilityLifeExpectancy.FUEL_FARM,
                FacilityLifeExpectancy.STANDBY_GENERATOR,
                FacilityLifeExpectancy.STORAGE_FACILITY,
            ]
        ],
    )
    FIRE_PROTECTION = ("Fire Protection", 30, [])
    ELECTRIC = (
        "Electric",
        40,
        [
            f
            for f in FacilityLifeExpectancy
            if f != FacilityLifeExpectancy.EQUIPMENT_PAD
        ],
    )
    FURNISHING = (
        "Furnishing",
        20,
        [
            f
            for f in FacilityLifeExpectancy
            if f
            not in [
                FacilityLifeExpectancy.EQUIPMENT_PAD,
                FacilityLifeExpectancy.TRUCK_FILL_STAND,
                FacilityLifeExpectancy.ENTRY_CONTROL_POINT,
                FacilityLifeExpectancy.FUEL_FARM,
                FacilityLifeExpectancy.STANDBY_GENERATOR,
                FacilityLifeExpectancy.STORAGE_FACILITY,
            ]
        ],
    )
    PROTECTION = (
        "Protection",
        10,
        [
            f
            for f in FacilityLifeExpectancy
            if f != FacilityLifeExpectancy.EQUIPMENT_PAD
        ],
    )
    SPECIAL_CONSTRUCTION = (
        "Special construction",
        10,
        [
            FacilityLifeExpectancy.ANTENNA_SUPPORT_BUILDING,
            FacilityLifeExpectancy.COMMUNICATION_FACILITY,
            FacilityLifeExpectancy.POWER_GENERATION_FACILITY,
            FacilityLifeExpectancy.GROUND_TERMINAL_T1,
            FacilityLifeExpectancy.OPS_FACILITY_T1,
            FacilityLifeExpectancy.DATA_CENTER,
            FacilityLifeExpectancy.RECEIVER_STATION,
            FacilityLifeExpectancy.GROUND_MONITORING_STATION,
            FacilityLifeExpectancy.ADMIN_OFFICE,
            FacilityLifeExpectancy.CENTRAL_UTILITY_PLANT,
            FacilityLifeExpectancy.MAINTENANCE_SHOP,
            FacilityLifeExpectancy.RADOME_FACILITY,
        ],
    )
    IMPROVEMENTS = (
        "Improvements",
        10,
        [
            f
            for f in FacilityLifeExpectancy
            if f != FacilityLifeExpectancy.TRUCK_FILL_STAND
        ],
    )
    UTILITIES = (
        "Utilities",
        30,
        [
            f
            for f in FacilityLifeExpectancy
            if f
            not in [
                FacilityLifeExpectancy.EQUIPMENT_PAD,
                FacilityLifeExpectancy.ENTRY_CONTROL_POINT,
            ]
        ],
    )
    DISTRIBUTION = (
        "Distribution",
        30,
        [
            f
            for f in FacilityLifeExpectancy
            if f != FacilityLifeExpectancy.EQUIPMENT_PAD
        ],
    )
    OTHER_CONSTRUCTION = (
        "Other Construction",
        30,
        [
            f
            for f in FacilityLifeExpectancy
            if f != FacilityLifeExpectancy.EQUIPMENT_PAD
        ],
    )
    SPECIAL_CONSTRUCTION2 = (
        "Special construction2",
        30,
        [
            f
            for f in FacilityLifeExpectancy
            if f != FacilityLifeExpectancy.EQUIPMENT_PAD
        ],
    )

    def __init__(self, label, life_expectancy, facilities):
        self.label = label
        self.life_expectancy = life_expectancy
        self.facilities = facilities
