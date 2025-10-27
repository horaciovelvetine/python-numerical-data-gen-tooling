#!/usr/bin/env python3
"""
Simple example of using the main.py functions directly.
"""

import sys
import os

# Add src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import get_random_facility_data_nums

# Generate data for a Data Center
facility = get_random_facility_data_nums("Data Center")

print("Generated facility data:")
print(f"Title: {facility.title}")
print(f"Age: {facility.age_in_years} years")
print(f"Condition Index: {facility.condition_index}")
print(f"Estimated Remaining Service Life: {facility.estimated_remaining_service_life:.2f} years")
print(f"Expected Service Life: {facility.expected_service_life} years")

# Print the facility as a dictionary
print("\nFull data structure:")
print(facility.to_dict())