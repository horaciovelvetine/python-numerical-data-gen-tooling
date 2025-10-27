#!/usr/bin/env python3
"""
Complete simulation runner for the python-numerical-data-gen-tooling project.
This script demonstrates various ways to run the simulation on the v1-work-eva branch.
"""

import json
import random
import time
from typing import List, Dict, Any

from const.facility_life_expectancy import FacilityLifeExpectancy
from ep_generate_random_facility_data import get_random_facility_data_nums_ep


def run_single_facility_simulation(facility_title: str, n_agents: int = 200, months_horizon: int = 120, seed: int = None) -> Dict[str, Any]:
    """
    Run simulation for a single facility type.
    
    Args:
        facility_title: Name of the facility type
        n_agents: Number of Monte Carlo agents to simulate
        months_horizon: Number of months to project forward
        seed: Random seed for reproducibility
    
    Returns:
        Dictionary containing the facility data
    """
    print(f"\n{'='*60}")
    print(f"Running simulation for: {facility_title}")
    print(f"Agents: {n_agents}, Horizon: {months_horizon} months")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        facility = get_random_facility_data_nums_ep(
            facility_title=facility_title,
            n_agents=n_agents,
            months_horizon=months_horizon,
            seed=seed
        )
        
        end_time = time.time()
        
        print(f"✓ Simulation completed in {end_time - start_time:.2f} seconds")
        print(f"  - Facility: {facility.title}")
        print(f"  - Age: {facility.age_in_years:.1f} years")
        print(f"  - Condition Index: {facility.condition_index:.3f}")
        print(f"  - Estimated Remaining Service Life: {facility.estimated_remaining_service_life:.1f} years")
        print(f"  - Expected Service Life: {facility.expected_service_life} years")
        
        return facility.to_dict()
        
    except Exception as e:
        print(f"✗ Error running simulation: {e}")
        return None


def run_batch_simulation(facility_count: int = 5, n_agents: int = 100, months_horizon: int = 120, seed: int = None) -> List[Dict[str, Any]]:
    """
    Run simulations for multiple random facility types.
    
    Args:
        facility_count: Number of different facilities to simulate
        n_agents: Number of Monte Carlo agents per facility
        months_horizon: Number of months to project forward
        seed: Random seed for reproducibility
    
    Returns:
        List of facility data dictionaries
    """
    print(f"\n{'='*60}")
    print(f"Running batch simulation for {facility_count} facilities")
    print(f"Agents per facility: {n_agents}, Horizon: {months_horizon} months")
    print(f"{'='*60}")
    
    # Get random sample of facilities
    all_facilities = list(FacilityLifeExpectancy)
    if seed:
        random.seed(seed)
    selected_facilities = random.sample(all_facilities, min(facility_count, len(all_facilities)))
    
    results = []
    total_start_time = time.time()
    
    for i, facility_enum in enumerate(selected_facilities, 1):
        print(f"\n[{i}/{len(selected_facilities)}] Processing: {facility_enum.title}")
        
        try:
            facility = get_random_facility_data_nums_ep(
                facility_title=facility_enum.title,
                n_agents=n_agents,
                months_horizon=months_horizon,
                seed=seed + i if seed else None
            )
            
            result = facility.to_dict()
            results.append(result)
            
            print(f"  ✓ Age: {facility.age_in_years:.1f}y, CI: {facility.condition_index:.3f}, RSL: {facility.estimated_remaining_service_life:.1f}y")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    total_end_time = time.time()
    
    print(f"\n{'='*60}")
    print(f"Batch simulation completed in {total_end_time - total_start_time:.2f} seconds")
    print(f"Successfully generated {len(results)} out of {facility_count} facilities")
    print(f"{'='*60}")
    
    return results


def run_comprehensive_demo():
    """
    Run a comprehensive demonstration of the simulation capabilities.
    """
    print("🏢 COMPREHENSIVE FACILITY SIMULATION DEMO")
    print("=" * 80)
    
    # Set seed for reproducible results
    demo_seed = 42
    
    # 1. List available facilities
    print("\n📋 Available Facility Types:")
    print("-" * 40)
    for facility in FacilityLifeExpectancy:
        print(f"  • {facility.title} (Expected Life: {facility.life_expectancy} years)")
    
    # 2. Run single facility simulation
    print("\n🎯 Single Facility Simulation:")
    single_result = run_single_facility_simulation(
        facility_title="Data Center",
        n_agents=300,
        months_horizon=240,  # 20 years
        seed=demo_seed
    )
    
    # 3. Run batch simulation
    print("\n🔄 Batch Facility Simulation:")
    batch_results = run_batch_simulation(
        facility_count=3,
        n_agents=150,
        months_horizon=120,  # 10 years
        seed=demo_seed
    )
    
    # 4. Save results
    all_results = {
        "single_facility": single_result,
        "batch_facilities": batch_results,
        "simulation_metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "seed": demo_seed,
            "total_facilities": len(batch_results) + (1 if single_result else 0)
        }
    }
    
    output_file = "comprehensive_simulation_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return all_results


def run_performance_test():
    """
    Run a performance test with different agent counts.
    """
    print("\n⚡ PERFORMANCE TEST")
    print("=" * 50)
    
    facility_title = "Office Building"
    agent_counts = [50, 100, 200, 500]
    
    performance_results = []
    
    for agent_count in agent_counts:
        print(f"\nTesting with {agent_count} agents...")
        
        start_time = time.time()
        
        try:
            facility = get_random_facility_data_nums_ep(
                facility_title=facility_title,
                n_agents=agent_count,
                months_horizon=120,
                seed=42
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            performance_results.append({
                "agent_count": agent_count,
                "duration_seconds": round(duration, 3),
                "facility_title": facility_title,
                "success": True
            })
            
            print(f"  ✓ Completed in {duration:.3f} seconds")
            
        except Exception as e:
            performance_results.append({
                "agent_count": agent_count,
                "duration_seconds": None,
                "facility_title": facility_title,
                "success": False,
                "error": str(e)
            })
            print(f"  ✗ Failed: {e}")
    
    # Save performance results
    with open("performance_test_results.json", 'w') as f:
        json.dump(performance_results, f, indent=2)
    
    print(f"\n📊 Performance test results saved to: performance_test_results.json")
    
    return performance_results


def main():
    """
    Main function to run different simulation modes.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Complete simulation runner for facility data generation")
    parser.add_argument('--mode', choices=['demo', 'single', 'batch', 'performance'], 
                       default='demo', help='Simulation mode to run')
    parser.add_argument('--facility', type=str, help='Facility title for single mode')
    parser.add_argument('--agents', type=int, default=200, help='Number of agents')
    parser.add_argument('--horizon', type=int, default=120, help='Months horizon')
    parser.add_argument('--count', type=int, default=5, help='Number of facilities for batch mode')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    if args.mode == 'demo':
        run_comprehensive_demo()
    elif args.mode == 'single':
        if not args.facility:
            print("Error: --facility is required for single mode")
            return
        run_single_facility_simulation(args.facility, args.agents, args.horizon, args.seed)
    elif args.mode == 'batch':
        run_batch_simulation(args.count, args.agents, args.horizon, args.seed)
    elif args.mode == 'performance':
        run_performance_test()


if __name__ == "__main__":
    main()