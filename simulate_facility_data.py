"""
Synthetic Facility Data Generator for US Space Infrastructure

This script reads an Excel workbook template and generates synthetic facility 
and system data following specified statistical distributions for predictive 
modeling of facility degradation and failure.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuration
EXCEL_FILE = '29 Oct - Simulate Data - US Space Template.xlsx'
N_FACILITIES = 1000
USE_REALISTIC_SITE_NAMES = False
MIN_FACILITIES_PER_SITE = 8

print("Loading Excel workbook...")
xl = pd.ExcelFile(EXCEL_FILE)

print("Parsing Key sheet for facility and system life expectancies...")
key_df = pd.read_excel(xl, sheet_name='Key', header=None)

# Parse facility types and life expectancies
facility_life = {}
facility_codes = {}

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

# Parse system types and life expectancies
system_life = {}

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

print(f"Found {len(facility_life)} facility types with life expectancies")
print(f"Found {len(system_life)} system types with life expectancies")
print(f"\nFacility types: {list(facility_life.keys())}")
print(f"\nSystem types: {list(system_life.keys())}")

def sample_age(expected_life: int) -> int:
    """
    Generate facility age using weighted distribution:
    - 50%: 20-40 years, 20%: 10-20 years, 20%: 41-80 years, 10%: 1-9 years
    
    Note: Facilities with life expectancy < 41 years are redistributed to other buckets.
    """
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


def sample_condition_index() -> int:
    """
    Generate condition index: 7% below 50, 88% between 50-85, 5% above 85.
    Range: 1-99
    """
    rand = np.random.random()
    
    if rand < 0.07:
        ci = np.random.randint(1, 50)
    elif rand < 0.95:
        ci = np.random.randint(50, 86)
    else:
        ci = np.random.randint(86, 100)
    
    return ci


def sample_remaining_service(age: int, expected_life: int) -> float:
    """
    Compute remaining service life: (expected_life - age) + N(0, 5), clipped to [0, 150].
    """
    base_remaining = expected_life - age
    noise = np.random.normal(0, 5)
    remaining = max(0, min(150, base_remaining + noise))
    return round(remaining, 2)


def compute_degradation_flag(remaining_service_life: float, condition_index: int) -> int:
    """
    Degraded if remaining service life < 5 years OR condition index < 50.
    """
    return 1 if remaining_service_life < 5 or condition_index < 50 else 0


def sample_mission_criticality() -> int:
    """Sample mission criticality uniformly between 3-9."""
    return np.random.randint(3, 10)


def get_mission_weight(facility_type: str) -> float:
    """
    Mission weights: Ops=3x, Critical infrastructure=2x, Others=1x
    """
    facility_lower = facility_type.lower()
    
    if 'ops' in facility_lower or 'operations' in facility_lower:
        return 3.0
    elif any(keyword in facility_lower for keyword in 
             ['data center', 'power generation', 'heating', 'cooling', 
              'generator', 'substation', 'switching', 'communication']):
        return 2.0
    else:
        return 1.0


print("\nGenerating synthetic facility data...")

records = []
dependency_chains = list(set(facility_codes.values())) or ['S1', 'S2', 'S3', 'S123', 'P1', 'P2', 'P3']
facility_types = list(facility_life.keys())
system_types = list(system_life.keys())

# Configure site names
if USE_REALISTIC_SITE_NAMES:
    site_names = ['Mars AFB', 'Jupiter Station', 'Saturn Base', 'Venus Outpost', 
                  'Neptune Facility', 'Uranus Station', 'Mercury Base', 'Pluto Outpost',
                  'Titan Station', 'Europa Base']
else:
    site_names = [f'Site {chr(65 + i)}' for i in range(10)]

installation_names = [f'Installation {i}' for i in range(1, 11)]

# Ensure each site has at least MIN_FACILITIES_PER_SITE facilities
site_assignments = []
n_sites = len(site_names)

for site_idx in range(n_sites):
    site_assignments.extend([site_idx] * MIN_FACILITIES_PER_SITE)

remaining_facilities = N_FACILITIES - len(site_assignments)
if remaining_facilities > 0:
    site_assignments.extend(np.random.choice(n_sites, size=remaining_facilities, replace=True))

np.random.shuffle(site_assignments)

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
        system_conditions[f'system_{system_type.lower().replace(" ", "_")}_ci'] = sample_condition_index()
    
    record = {
        'site': site, 'installation': installation, 'mission_criticality': mission_criticality,
        'mission_weight': mission_weight, 'facility_type': facility_type,
        'facility_number': facility_number, 'year_constructed': year_constructed,
        'age_years': age, 'expected_life': expected_life, 'condition_index': condition_index,
        'remaining_service_life': remaining_service, 'dependency_chain': dependency_chain,
        'degradation_flag': degradation,
    }
    record.update(system_conditions)
    records.append(record)
    
    if (i + 1) % 100 == 0:
        print(f"Generated {i + 1}/{N_FACILITIES} facilities...")

print("\nCreating DataFrame...")
df = pd.DataFrame(records)

print("\n" + "="*80)
print("SYNTHETIC FACILITY DATA SUMMARY")
print("="*80)
print(f"\nTotal facilities generated: {len(df)}")
print(f"\nDataFrame shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")

print("\n--- Distribution Validation ---")
print(f"\nAge distribution:")
print(f"  1-9 years: {((df['age_years'] >= 1) & (df['age_years'] < 10)).sum()} ({((df['age_years'] >= 1) & (df['age_years'] < 10)).mean()*100:.1f}%) [Target: 10%]")
print(f"  10-20 years: {((df['age_years'] >= 10) & (df['age_years'] <= 20)).sum()} ({((df['age_years'] >= 10) & (df['age_years'] <= 20)).mean()*100:.1f}%) [Target: 20%]")
print(f"  20-40 years: {((df['age_years'] >= 20) & (df['age_years'] <= 40)).sum()} ({((df['age_years'] >= 20) & (df['age_years'] <= 40)).mean()*100:.1f}%) [Target: 50%]")
print(f"  41-80 years: {((df['age_years'] >= 41) & (df['age_years'] <= 80)).sum()} ({((df['age_years'] >= 41) & (df['age_years'] <= 80)).mean()*100:.1f}%) [Target: 20%]")
print(f"  Zero-year facilities: {(df['age_years'] == 0).sum()} (should be 0)")
print(f"\n  Note: The 41-80 age range is constrained by facility life expectancies.")
print(f"  {(df['expected_life'] < 41).sum()} facilities ({(df['expected_life'] < 41).mean()*100:.1f}%) have life expectancy < 41 years,")
print(f"  making it impossible for them to reach the 41+ age range.")
print(f"  This is a structural constraint of the facility types in the workbook.")

print(f"\nCondition Index distribution:")
print(f"  Below 50: {(df['condition_index'] < 50).sum()} ({(df['condition_index'] < 50).mean()*100:.1f}%) [Target: 7%]")
print(f"  50-85: {((df['condition_index'] >= 50) & (df['condition_index'] <= 85)).sum()} ({((df['condition_index'] >= 50) & (df['condition_index'] <= 85)).mean()*100:.1f}%) [Target: 88%]")
print(f"  Above 85: {(df['condition_index'] > 85).sum()} ({(df['condition_index'] > 85).mean()*100:.1f}%) [Target: 5%]")

print(f"\nDegradation flags:")
print(f"  Degraded (flag=1): {(df['degradation_flag'] == 1).sum()} ({(df['degradation_flag'] == 1).mean()*100:.1f}%)")
print(f"  Normal (flag=0): {(df['degradation_flag'] == 0).sum()} ({(df['degradation_flag'] == 0).mean()*100:.1f}%)")

print(f"\nMission Criticality distribution:")
print(df['mission_criticality'].value_counts().sort_index())

print(f"\nFacility Types distribution (top 10):")
print(df['facility_type'].value_counts().head(10))

print(f"\nSite distribution (minimum {MIN_FACILITIES_PER_SITE} per site required):")
site_counts = df['site'].value_counts().sort_index()
print(site_counts)
min_site_count = site_counts.min()
print(f"  Minimum facilities at any site: {min_site_count} {'✅' if min_site_count >= MIN_FACILITIES_PER_SITE else '❌'}")

print("\n--- Descriptive Statistics ---")
print(df[['age_years', 'condition_index', 'remaining_service_life', 'mission_criticality', 'mission_weight', 'degradation_flag']].describe())

print("\n--- First 10 records ---")
print(df.head(10).to_string())

output_file = 'simulated_facility_data.csv'
print(f"\nSaving data to {output_file}...")
df.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print(f"SUCCESS! Synthetic facility data saved to: {output_file}")
print(f"{'='*80}")
print("\nThis dataset can be used to train predictive models for:")
print("  - Facility degradation prediction")
print("  - Failure risk estimation")
print("  - Maintenance prioritization")
print("  - Resource allocation optimization")
print("\nKey features for modeling:")
print("  - age_years: Current age of facility")
print("  - condition_index: Overall facility condition (1-99)")
print("  - remaining_service_life: Estimated remaining years")
print("  - mission_criticality: Mission importance (3-9)")
print("  - mission_weight: Facility importance multiplier")
print("  - system_*_ci: Condition indices for individual systems")
print("  - degradation_flag: Target variable (1=degraded, 0=normal)")

