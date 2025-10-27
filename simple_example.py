#!/usr/bin/env python3
"""
Simple example of using the facility data generation functions directly.
"""

from ep_generate_random_facility_data import get_random_facility_data_nums_ep

# Generate data for a Data Center
facility = get_random_facility_data_nums_ep("Data Center")

print("Generated facility data:")
print(f"Title: {facility.title}")
print(f"Age: {facility.age_in_years} years")
print(f"Condition Index: {facility.condition_index}")
print(f"Estimated Remaining Service Life: {facility.estimated_remaining_service_life:.2f} years")
print(f"Expected Service Life: {facility.expected_service_life} years")

# Print the facility as a dictionary
print("\nFull data structure:")
print(facility.to_dict())