#!/usr/bin/env python3
"""
Demo script to show how to run the facility data generation simulation.
"""

import json
from ep_generate_random_facility_data import get_random_facility_data_nums_ep
from const.facility_life_expectancy import FacilityLifeExpectancy


def demo_single_facility(facility_title: str):
    """Generate data for a single facility type."""
    print(f"\n=== Generating data for: {facility_title} ===")
    
    try:
        facility = get_random_facility_data_nums_ep(facility_title)
        
        print(f"Facility: {facility.title}")
        print(f"Age: {facility.age_in_years} years")
        print(f"Expected Service Life: {facility.expected_service_life} years")
        print(f"Current Condition Index: {facility.condition_index:.2f}")
        print(f"Estimated Remaining Service Life: {facility.estimated_remaining_service_life:.2f} years")
        # Show time series data structure
        if facility.time_series:
            print(f"Time Series Data:")
            if 'year' in facility.time_series:
                years = sorted(facility.time_series['year'].keys())
                print(f"  Yearly data points: {len(years)}")
                for year in years:
                    condition = facility.time_series['year'][year]
                    if condition is not None:
                        print(f"    Year {year}: {condition:.2f}")
            
            if 'months' in facility.time_series:
                months = sorted(facility.time_series['months'].keys())
                print(f"  Monthly data points: {len(months)}")
                # Show only first few months to avoid too much output
                for month in months[:5]:
                    condition = facility.time_series['months'][month]
                    if condition is not None:
                        print(f"    Month {month}: {condition:.2f}")
                if len(months) > 5:
                    print(f"    ... and {len(months) - 5} more monthly data points")
        
        return facility
        
    except Exception as e:
        print(f"Error generating data for '{facility_title}': {e}")
        return None


def demo_multiple_facilities(count: int = 5):
    """Generate data for multiple random facility types."""
    print(f"\n=== Generating data for {count} random facilities ===")
    
    # Get all available facility types
    all_facilities = list(FacilityLifeExpectancy)
    
    import random
    selected_facilities = random.sample(all_facilities, min(count, len(all_facilities)))
    
    results = []
    for facility_enum in selected_facilities:
        facility_data = demo_single_facility(facility_enum.title)
        if facility_data:
            results.append(facility_data)
    
    return results


def list_available_facilities():
    """List all available facility types."""
    print("\n=== Available Facility Types ===")
    for i, facility in enumerate(FacilityLifeExpectancy, 1):
        print(f"{i:2d}. {facility.title} (Life Expectancy: {facility.life_expectancy} years)")


def save_results_to_json(facilities, filename="simulation_results.json"):
    """Save facility data to JSON file."""
    data = [facility.to_dict() for facility in facilities]
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nResults saved to: {filename}")


def main():
    """Main demo function."""
    print("=== Facility Data Generation Simulation Demo ===")
    
    # List available facilities
    list_available_facilities()
    
    # Demo with a specific facility
    demo_single_facility("Data Center")
    
    # Demo with multiple random facilities
    facilities = demo_multiple_facilities(3)
    
    # Save results to JSON
    if facilities:
        save_results_to_json(facilities)
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()