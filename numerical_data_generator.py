import numpy as np
import pandas as pd
from typing import Dict, Union, Optional
import os
import re
from pathlib import Path

# Uses np.random.randint(), np.random.uniform(), np.random.normal() to generate random values
# Each facility gets random: age, condition index, facility type, facility number
# Random noise is added to remaining service life calculations

# Import life expectancy data from const folder
try:
    from const.facility_life_expectancy import facility_life_expectancy_data
    from const.systems_life_expectancy import systems_life_expectancy_data
except ImportError as error:
    raise ImportError("Could not import life expectancy data from const folder") from error

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'V_1_Dataset')
OUTPUT_BASE_FILENAME = 'generated_facility_data'


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

# ============================================================================
# CORE GENERATION FUNCTIONS
# ============================================================================

# Centralizes random numerical sampling for downstream simulation workflows.
def generate_numerical_data(
    n: int,
    min_val: float,
    max_val: float,
    mean: Optional[float] = None,
    std_dev: Optional[float] = None,
    distribution: str = 'uniform',
    data_type: str = 'int'
) -> np.ndarray:
    """
    Generate n rows of numerical data with specified parameters.
    
    Args:
        n: Number of rows to generate
        min_val: Minimum value
        max_val: Maximum value
        mean: Target mean (optional, used for normal distribution)
        std_dev: Standard deviation (optional, used for normal distribution)
        distribution: Type of distribution ('uniform', 'normal', 'custom')
        data_type: Output type ('int' or 'float')
        
    Returns:
        Array of generated values
    """
    if distribution == 'uniform':
        if data_type == 'int':
            data = np.random.randint(min_val, max_val + 1, size=n)
        else:
            data = np.random.uniform(min_val, max_val, size=n)
            
    elif distribution == 'normal':
        if mean is None:
            mean = (min_val + max_val) / 2
        if std_dev is None:
            std_dev = (max_val - min_val) / 6
            
        data = np.random.normal(mean, std_dev, size=n)
        data = np.clip(data, min_val, max_val)
        
        if data_type == 'int':
            data = data.astype(int)
            
    else:
        raise ValueError(f"Unknown distribution: {distribution}")
        
    return data


# ============================================================================
# AGE GENERATION
# ============================================================================

# Enforces realistic facility age distributions aligned with lifecycle targets.
def generate_age_data(n: int, expected_life: Optional[int] = None) -> np.ndarray:
    """
    Generate facility age data with specified distribution.
    
    Distribution:
    - 50%: 20-40 years
    - 20%: 10-20 years
    - 20%: 41+ years (capped at 80 or expected_life)
    - 10%: 1-9 years
    
    Args:
        n: Number of age values to generate
        expected_life: Expected life for capping (optional, default 80)
        
    Returns:
        Array of age values
    """
    if expected_life is None:
        expected_life = 80
        
    ages = np.zeros(n, dtype=int)
    
    for i in range(n):
        rand = np.random.random()
        
        if rand < 0.50:  # 50%: 20-40 years
            age = np.random.randint(20, 41)
        elif rand < 0.70:  # 20%: 10-20 years
            age = np.random.randint(10, 21)
        elif rand < 0.90:  # 20%: 41+ years
            upper_bound = min(expected_life, 80)
            if upper_bound < 41:
                # If life expectancy is too low, redistribute
                age = np.random.randint(20, min(41, upper_bound + 1))
            else:
                age = np.random.randint(41, upper_bound + 1)
        else:  # 10%: 1-9 years
            age = np.random.randint(1, 10)
            
        # Cap at expected life
        age = min(age, expected_life, 80)
        age = max(1, age)
        ages[i] = age
        
    return ages


# ============================================================================
# CONDITION INDEX GENERATION
# ============================================================================

# Keeps facility condition scores aligned with desired portfolio performance.
def generate_condition_index(
    n: int,
    target_mean: float = 70,
    adjust_for_mean: bool = True
) -> np.ndarray:
    """
    Generate condition index values with specified distribution.
    
    Distribution:
    - 7% below 50
    - 88% between 50-85 (remainder)
    - 5% above 85
    Range: 1-99
    Target mean: 70
    
    Args:
        n: Number of values to generate
        target_mean: Target mean value (default 70)
        adjust_for_mean: Whether to adjust values to hit target mean
        
    Returns:
        Array of condition index values
    """
    conditions = np.zeros(n, dtype=int)
    
    for i in range(n):
        rand = np.random.random()
        
        if rand < 0.07:  # 7%: below 50
            ci = np.random.randint(1, 50)
        elif rand < 0.95:  # 88%: 50-85
            ci = np.random.randint(50, 86)
        else:  # 5%: above 85
            ci = np.random.randint(86, 100)
            
        conditions[i] = ci
    
    # Adjust to hit target mean if requested
    if adjust_for_mean:
        current_mean = conditions.mean()
        adjustment = target_mean - current_mean
        
        if abs(adjustment) > 1:
            # Apply adjustment to middle range values
            middle_mask = (conditions >= 50) & (conditions <= 85)
            conditions[middle_mask] = np.clip(
                conditions[middle_mask] + int(adjustment),
                50, 85
            )
    
    return conditions


# ============================================================================
# REMAINING SERVICE LIFE CALCULATION
# ============================================================================

# Converts current age into remaining service life with optional uncertainty.
def calculate_remaining_service_life(
    ages: np.ndarray,
    life_expectancies: Union[int, np.ndarray],
    add_noise: bool = True,
    noise_std: float = 5.0
) -> np.ndarray:
    """
    Calculate remaining service life.
    
    Formula: Remaining = Life Expectancy - Age + noise
    
    Args:
        ages: Array of facility ages
        life_expectancies: Expected life (single value or array)
        add_noise: Whether to add Gaussian noise
        noise_std: Standard deviation of noise (default 5.0)
        
    Returns:
        Array of remaining service life values
    """
    if isinstance(life_expectancies, int):
        life_expectancies = np.full(len(ages), life_expectancies)
        
    remaining = life_expectancies - ages
    
    if add_noise:
        noise = np.random.normal(0, noise_std, size=len(ages))
        remaining = remaining + noise
        
    # Clip to [0, 150]
    remaining = np.clip(remaining, 0, 150)
    
    return remaining


# ============================================================================
# CONDITION INDEX TIME SERIES
# ============================================================================

# Reconstructs historical condition trends to support time-series analysis.
def generate_condition_time_series(
    current_condition: int,
    n_months: int = 120,
    decay_rate: float = 0.005,
    initial_condition: int = 99
) -> pd.DataFrame:
    """
    Generate historical condition data using decay function.
    
    Formula: A = P * (1 - R)^t
    Where:
        A = Condition at time t
        P = Initial condition (99 at installation)
        R = Decay rate
        t = Time periods (months)
        
    Args:
        current_condition: Current condition index
        n_months: Number of months to generate (default 120 = 10 years)
        decay_rate: Rate of decay per month
        initial_condition: Condition at installation (default 99)
        
    Returns:
        DataFrame with columns: month, condition_index, date
    """
    # Calculate decay rate to reach current condition
    # current_condition = initial_condition * (1 - R)^n_months
    # Solve for R if needed
    if current_condition < initial_condition:
        implied_rate = 1 - (current_condition / initial_condition) ** (1 / n_months)
        decay_rate = max(decay_rate, implied_rate)
    
    # Generate time series going backwards from current
    months = np.arange(-n_months, 1)  # -120 to 0 (current)
    
    # Calculate conditions at each time point
    # Going backwards: higher condition in the past
    conditions = []
    for month in months:
        # For past months (negative), we reverse the decay
        if month < 0:
            # Reverse decay: condition was higher in the past
            t_from_install = n_months + month  # How long ago was installation
            condition = initial_condition * (1 - decay_rate) ** t_from_install
        else:
            condition = current_condition
            
        conditions.append(int(np.clip(condition, 1, 99)))
    
    # Create DataFrame
    from datetime import datetime, timedelta
    current_date = datetime.now()
    dates = [current_date + timedelta(days=int(30 * m)) for m in months]
    
    df = pd.DataFrame({
        'month_offset': months,
        'condition_index': conditions,
        'date': dates
    })
    
    return df


# ============================================================================
# FACILITY NUMBER GENERATION
# ============================================================================

# Ensures datasets include unique identifiers across simulated facilities.
def generate_facility_numbers(n: int, start: int = 1, end: int = 9999) -> np.ndarray:
    """
    Generate unique facility numbers.
    
    Args:
        n: Number of facility numbers to generate
        start: Starting number (default 1)
        end: Ending number (default 9999)
        
    Returns:
        Array of unique facility numbers
    """
    return np.random.choice(range(start, end + 1), size=n, replace=False)


# ============================================================================
# COMPREHENSIVE DATASET GENERATION
# ============================================================================

# Combines individual generators into a cohesive facility-level dataset.
def generate_facility_dataset(
    n_facilities: int = 1000,
    include_time_series: bool = False
) -> pd.DataFrame:
    """
    Generate a complete facility dataset with all required fields.
    
    Args:
        n_facilities: Number of facilities to generate
        include_time_series: Whether to include historical time series
        
    Returns:
        DataFrame with facility data
    """
    # Get life expectancy data
    if facility_life_expectancy_data:
        facility_types = [f['label'] for f in facility_life_expectancy_data]
        life_expectancies = [f['life_expectancy'] for f in facility_life_expectancy_data]
    else:
        # Default values if const data not available
        facility_types = ['Generic Facility']
        life_expectancies = [40]
    
    records = []
    
    for i in range(n_facilities):
        # Random facility type
        facility_idx = np.random.randint(0, len(facility_types))
        facility_type = facility_types[facility_idx]
        expected_life = life_expectancies[facility_idx]
        
        # Generate age
        age = generate_age_data(1, expected_life)[0]
        
        # Generate condition index
        condition_idx = generate_condition_index(1, target_mean=70)[0]
        
        # Calculate remaining service life
        remaining = calculate_remaining_service_life(
            np.array([age]),
            np.array([expected_life])
        )[0]
        
        # Generate facility number
        facility_num = np.random.randint(1, 10000)
        
        record = {
            'facility_number': facility_num,
            'facility_type': facility_type,
            'age_years': age,
            'expected_life_years': expected_life,
            'condition_index': condition_idx,
            'remaining_service_life': round(remaining, 2),
            'year_constructed': 2025 - age
        }
        
        # Add time series if requested
        if include_time_series:
            time_series = generate_condition_time_series(
                condition_idx,
                n_months=120
            )
            record['condition_history'] = time_series.to_dict('records')
        
        records.append(record)
        
    df = pd.DataFrame(records)
    
    return df


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dataset = generate_facility_dataset(n_facilities=1000, include_time_series=False)
    output_path = get_versioned_output_path(OUTPUT_DIR, OUTPUT_BASE_FILENAME)
    dataset.to_csv(output_path, index=False)

