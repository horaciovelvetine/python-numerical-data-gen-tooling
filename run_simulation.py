#!/usr/bin/env python3
"""
Command-line interface for facility data generation.
"""

import sys
import os
import json
import argparse

# Import the Eva Pavlik implementation
from ep_generate_random_facility_data import get_random_facility_data_nums_ep
from const.facility_life_expectancy import FacilityLifeExpectancy


def generate_single_facility(facility_title: str, output_file: str = None):
    """Generate data for a single facility."""
    try:
        facility = get_random_facility_data_nums_ep(facility_title)
        
        result = facility.to_dict()
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Data saved to: {output_file}")
        else:
            print(json.dumps(result, indent=2))
            
        return facility
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def generate_multiple_facilities(count: int, output_file: str = None):
    """Generate data for multiple random facilities."""
    import random
    
    all_facilities = list(FacilityLifeExpectancy)
    selected_facilities = random.sample(all_facilities, min(count, len(all_facilities)))
    
    results = []
    for facility_enum in selected_facilities:
        try:
            facility = get_random_facility_data_nums_ep(facility_enum.title)
            results.append(facility.to_dict())
        except Exception as e:
            print(f"Error generating data for '{facility_enum.title}': {e}", file=sys.stderr)
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Generated {len(results)} facilities, saved to: {output_file}")
    else:
        print(json.dumps(results, indent=2))


def list_facilities():
    """List all available facility types."""
    print("Available facility types:")
    for facility in FacilityLifeExpectancy:
        print(f"- {facility.title} (Life Expectancy: {facility.life_expectancy} years)")


def main():
    parser = argparse.ArgumentParser(description="Generate random facility data")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available facility types')
    
    # Single facility command
    single_parser = subparsers.add_parser('single', help='Generate data for a single facility')
    single_parser.add_argument('facility_title', help='Title of the facility type')
    single_parser.add_argument('-o', '--output', help='Output file (JSON)')
    
    # Multiple facilities command
    multi_parser = subparsers.add_parser('multiple', help='Generate data for multiple random facilities')
    multi_parser.add_argument('count', type=int, help='Number of facilities to generate')
    multi_parser.add_argument('-o', '--output', help='Output file (JSON)')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_facilities()
    elif args.command == 'single':
        generate_single_facility(args.facility_title, args.output)
    elif args.command == 'multiple':
        generate_multiple_facilities(args.count, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()