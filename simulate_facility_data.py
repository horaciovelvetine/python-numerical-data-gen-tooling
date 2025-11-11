import os
import re
import warnings
from pathlib import Path
from typing import Dict, Tuple, List
import numpy as np
import pandas as pd

# Uses np.random.choice() to randomly select facility types, sites, installations
# Uses np.random.randint() for ages, condition indices, facility numbers
# Uses np.random.normal() for noise in remaining service life

warnings.filterwarnings('ignore')

# Configuration
EXCEL_FILE = '29 Oct - Simulate Data - US Space Template.xlsx'
N_FACILITIES = 1000
USE_REALISTIC_SITE_NAMES = False
MIN_FACILITIES_PER_SITE = 8

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'V_1_Dataset')
OUTPUT_BASE_FILENAME = 'simulated_facility_data'


# Determines the next versioned CSV filename within the output directory.
def get_versioned_output_path(output_dir: str, base_filename: str) -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    pattern = re.compile(rf"{re.escape(base_filename)}_V_(\d+)\.csv$")
    max_version = 0

    for file_path in directory.glob(f"{base_filename}_V_*.csv"):
        match = pattern.match(file_path.name)
        if match:
            version = int(match.group(1))
            if version > max_version:
                max_version = version

    next_version = max_version + 1
    return directory / f"{base_filename}_V_{next_version}.csv"


# Centralizes workbook parsing so every run uses the same life-expectancy baselines.
def load_life_expectancy_tables(
    excel_file: str
) -> Tuple[Dict[str, int], Dict[str, str], Dict[str, int]]:
    xl = pd.ExcelFile(excel_file)
    key_df = pd.read_excel(xl, sheet_name='Key', header=None)

    facility_life: Dict[str, int] = {}
    facility_codes: Dict[str, str] = {}
    for idx in range(4, len(key_df)):
        try:
            row = key_df.iloc[idx]
            if pd.notna(row[1]) and pd.notna(row[4]):
                facility_name = str(row[1]).strip()
                life_exp = int(float(row[4]))
                dependency_code = str(row[3]).strip() if pd.notna(row[3]) else "S1"
                facility_life[facility_name] = life_exp
                facility_codes[facility_name] = dependency_code
        except (ValueError, TypeError):
            continue

    system_life: Dict[str, int] = {}
    for idx in range(4, 30):
        try:
            if idx < len(key_df):
                row = key_df.iloc[idx]
                if pd.notna(row[7]) and pd.notna(row[8]):
                    system_name = str(row[7]).strip()
                    life_exp = int(float(row[8]))
                    system_life[system_name] = life_exp
        except (ValueError, TypeError):
            continue

    return facility_life, facility_codes, system_life


# Maintains consistent age behavior across facility types while respecting caps.
def sample_age(expected_life: int) -> int:
    rand = np.random.random()

    if rand < 0.50:
        age = np.random.randint(20, 41)
    elif rand < 0.70:
        age = np.random.randint(10, 21)
    elif rand < 0.90:
        upper_bound = min(expected_life, 80)
        if upper_bound < 41:
            resample = np.random.random()
            if resample < 0.625:
                age = np.random.randint(20, min(41, upper_bound + 1))
            elif resample < 0.875:
                age = np.random.randint(10, 21)
            else:
                age = np.random.randint(1, 10)
        else:
            age = np.random.randint(41, upper_bound + 1)
    else:
        age = np.random.randint(1, 10)

    max_allowed_age = int(expected_life * 1.2)
    age = min(age, max_allowed_age, 80)
    age = max(1, age)

    return age


# Keeps condition scoring aligned with enterprise readiness targets.
def sample_condition_index() -> int:
    rand = np.random.random()

    if rand < 0.07:
        ci = np.random.randint(1, 50)
    elif rand < 0.95:
        ci = np.random.randint(50, 86)
    else:
        ci = np.random.randint(86, 100)

    return ci


# Converts age into remaining service life while introducing uncertainty.
def sample_remaining_service(age: int, expected_life: int) -> float:
    base_remaining = expected_life - age
    noise = np.random.normal(0, 5)
    remaining = max(0, min(150, base_remaining + noise))
    return round(remaining, 2)


# Flags assets that require intervention under risk-informed rules.
def compute_degradation_flag(remaining_service_life: float, condition_index: int) -> int:
    return 1 if remaining_service_life < 5 or condition_index < 50 else 0


# Supports mission modeling by providing prioritization weights.
def sample_mission_criticality() -> int:
    return np.random.randint(3, 10)


# Maps facilities to operational weightings based on their role.
def get_mission_weight(facility_type: str) -> float:
    facility_lower = facility_type.lower()

    if 'ops' in facility_lower or 'operations' in facility_lower:
        return 3.0
    if any(keyword in facility_lower for keyword in
           ['data center', 'power generation', 'heating', 'cooling',
            'generator', 'substation', 'switching', 'communication']):
        return 2.0
    return 1.0


# Guarantees every site meets minimum representation while spreading the rest.
def create_site_assignments(site_names: List[str]) -> List[int]:
    assignments: List[int] = []
    n_sites = len(site_names)
    for site_idx in range(n_sites):
        assignments.extend([site_idx] * MIN_FACILITIES_PER_SITE)

    remaining_facilities = N_FACILITIES - len(assignments)
    if remaining_facilities > 0:
        assignments.extend(np.random.choice(n_sites, size=remaining_facilities, replace=True))

    np.random.shuffle(assignments)
    return assignments


# Builds fully-populated facility records ready for analytics.
def build_facility_dataframe(
    facility_life: Dict[str, int],
    facility_codes: Dict[str, str],
    system_life: Dict[str, int]
) -> pd.DataFrame:
    records = []
    dependency_chains = list(set(facility_codes.values())) or ['S1', 'S2', 'S3', 'S123', 'P1', 'P2', 'P3']
    facility_types = list(facility_life.keys())
    system_types = list(system_life.keys())

    if USE_REALISTIC_SITE_NAMES:
        site_names = [
            'Mars AFB', 'Jupiter Station', 'Saturn Base', 'Venus Outpost',
            'Neptune Facility', 'Uranus Station', 'Mercury Base', 'Pluto Outpost',
            'Titan Station', 'Europa Base'
        ]
    else:
        site_names = [f'Site {chr(65 + i)}' for i in range(10)]

    installation_names = [f'Installation {i}' for i in range(1, 11)]
    site_assignments = create_site_assignments(site_names)

    for i in range(N_FACILITIES):
        facility_type = np.random.choice(facility_types)
        expected_life = facility_life[facility_type]
        age = sample_age(expected_life)
        condition_index = sample_condition_index()
        remaining_service = sample_remaining_service(age, expected_life)
        degradation = compute_degradation_flag(remaining_service, condition_index)

        site = site_names[site_assignments[i]]
        installation = np.random.choice(installation_names)
        mission_criticality = sample_mission_criticality()
        facility_number = np.random.randint(1, 10000)
        dependency_chain = facility_codes.get(facility_type, np.random.choice(dependency_chains))
        mission_weight = get_mission_weight(facility_type)
        year_constructed = 2025 - age

        system_conditions = {}
        for system_type in system_types:
            key = f'system_{system_type.lower().replace(" ", "_")}_ci'
            system_conditions[key] = sample_condition_index()

        record = {
            'site': site,
            'installation': installation,
            'mission_criticality': mission_criticality,
            'mission_weight': mission_weight,
            'facility_type': facility_type,
            'facility_number': facility_number,
            'year_constructed': year_constructed,
            'age_years': age,
            'expected_life': expected_life,
            'condition_index': condition_index,
            'remaining_service_life': remaining_service,
            'dependency_chain': dependency_chain,
            'degradation_flag': degradation,
        }
        record.update(system_conditions)
        records.append(record)

    return pd.DataFrame(records)


# Coordinates end-to-end dataset generation and persistence.
def main() -> None:
    facility_life, facility_codes, system_life = load_life_expectancy_tables(EXCEL_FILE)
    dataset = build_facility_dataframe(facility_life, facility_codes, system_life)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = get_versioned_output_path(OUTPUT_DIR, OUTPUT_BASE_FILENAME)
    dataset.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()