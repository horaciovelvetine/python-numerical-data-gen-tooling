#!/usr/bin/env python3
"""
Quick start script for running simulations.
This is the easiest way to get started with the simulation.
"""

from ep_generate_random_facility_data import get_random_facility_data_nums_ep
import json

def quick_demo():
    """Run a quick demonstration of the simulation."""
    print("🚀 Quick Simulation Demo")
    print("=" * 40)
    
    # Generate data for a Data Center
    print("\nGenerating data for a Data Center...")
    facility = get_random_facility_data_nums_ep(
        facility_title="Data Center",
        n_agents=100,  # Use fewer agents for faster execution
        months_horizon=60,  # 5 years projection
        seed=42  # For reproducible results
    )
    
    print(f"\n✅ Simulation Complete!")
    print(f"📊 Results:")
    print(f"   • Facility: {facility.title}")
    print(f"   • Current Age: {facility.age_in_years:.1f} years")
    print(f"   • Condition Index: {facility.condition_index:.3f}")
    print(f"   • Estimated Remaining Service Life: {facility.estimated_remaining_service_life:.1f} years")
    print(f"   • Expected Total Service Life: {facility.expected_service_life} years")
    
    # Show some time series data
    if facility.time_series and 'year' in facility.time_series:
        print(f"\n📈 Condition Projection (by year):")
        for year, condition in facility.time_series['year'].items():
            if condition is not None:
                print(f"   Year {year}: {condition:.3f}")
    
    # Save to JSON file
    result = facility.to_dict()
    with open("quick_demo_results.json", 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Full results saved to: quick_demo_results.json")
    return result

if __name__ == "__main__":
    quick_demo()