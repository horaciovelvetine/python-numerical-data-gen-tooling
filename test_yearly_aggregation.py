#!/usr/bin/env python3
"""
Test script to verify the yearly aggregation fix.
"""

from ep_generate_random_facility_data import get_random_facility_data_nums_ep
import json

# Test with multiple runs to get different ages
print("Testing yearly data aggregation fix...")

for i in range(5):
    print(f"\nTest run {i+1}:")
    
    facility = get_random_facility_data_nums_ep(
        facility_title="Data Center",
        n_agents=50,  # Use fewer agents for faster execution
        months_horizon=60,  # 5 years projection
        seed=i  # Different seed each time
    )
    
    print(f"  Age: {facility.age_in_years} years")
    print(f"  Monthly data points: {len(facility.time_series['months'])}")
    
    # Check yearly data
    yearly_data = facility.time_series['year']
    non_null_years = [year for year, value in yearly_data.items() if value is not None]
    null_years = [year for year, value in yearly_data.items() if value is None]
    
    print(f"  Years with data: {non_null_years}")
    print(f"  Years with null: {null_years}")
    
    # Show some actual values
    for year in non_null_years[:3]:  # Show first 3 years with data
        print(f"    Year {year}: {yearly_data[year]:.3f}")

print("\n✅ Test completed!")