#!/usr/bin/env python3
"""
Debug script to understand the monthly data structure.
"""

from ep_generate_random_facility_data import get_random_facility_data_nums_ep
import json

facility = get_random_facility_data_nums_ep(
    facility_title="Data Center",
    n_agents=50,
    months_horizon=60,
    seed=1
)

print(f"Facility age: {facility.age_in_years} years")
print(f"Monthly data keys (first 10): {list(facility.time_series['months'].keys())[:10]}")
print(f"Monthly data key types: {[type(k) for k in list(facility.time_series['months'].keys())[:5]]}")

# Check what the range comparison looks like
months_data = facility.time_series['months']
print(f"\nFirst few month values:")
for i, (month, value) in enumerate(list(months_data.items())[:5]):
    print(f"  Month {month} (type: {type(month)}): {value}")

# Test the range logic manually
print(f"\nTesting range logic for year 0 (months 0-11):")
year_0_vals = []
for m, v in months_data.items():
    try:
        month_int = int(m)
        if 0 <= month_int <= 11:
            year_0_vals.append(v)
            print(f"  Found month {month_int} in year 0: {v}")
    except:
        print(f"  Error converting month {m} to int")

print(f"Year 0 values found: {len(year_0_vals)}")

# Test for a year that should have data
age_months = facility.age_in_years * 12
print(f"\nFacility is {facility.age_in_years} years old = {age_months} months")
print(f"So yearly data should start around year {age_months // 12}")

# Check the year that should contain data
target_year = age_months // 12
start_month = target_year * 12
end_month = start_month + 11
print(f"\nTesting year {target_year} (months {start_month}-{end_month}):")

target_year_vals = []
for m, v in months_data.items():
    month_int = int(m)
    if start_month <= month_int <= end_month:
        target_year_vals.append(v)
        print(f"  Found month {month_int}: {v}")

print(f"Values found for year {target_year}: {len(target_year_vals)}")
if target_year_vals:
    avg = sum(target_year_vals) / len(target_year_vals)
    print(f"Average: {avg:.3f}")