"""
Agent-based Monte Carlo generator for facility numerical data (Eva Pavlik's implementation).
Provides get_random_facility_data_nums_ep(...) and imports local ep_func helpers.
"""
from const.facility_life_expectancy import FacilityLifeExpectancy
from models.facility import Facility

from ep_rnd_age import ep_rnd_age
from ep_rnd_condition_index import ep_rnd_condition_index
from ep_agent_simulator import ep_agent_simulator
from ep_estimate_remaining_service_life import ep_estimate_remaining_service_life


def get_random_facility_data_nums_ep(facility_title: str, n_agents: int = 200, months_horizon: int = 120, seed: int | None = None) -> Facility:
    """
    Orchestrator for the agent-based Monte Carlo (Eva Pavlik's implementation).
    """
    if FacilityLifeExpectancy.is_valid_title(facility_title) is not True:
        raise ValueError(f"Unexpected facility title: '{facility_title}'")

    facility = FacilityLifeExpectancy.find_by_title(facility_title)

    # Sample initial deterministic values
    age_in_years = ep_rnd_age(facility, seed=seed)
    age_in_months = age_in_years * 12
    condition_index = ep_rnd_condition_index(seed=seed)

    # Run agent simulations
    agents = ep_agent_simulator(age_in_months, condition_index, facility, n_agents=n_agents, months_horizon=months_horizon, seed=seed)

    # Aggregate agent results to compute median trajectory and median RSL
    month_values = {}
    for agent in agents:
        for m, v in agent['months'].items():
            month_values.setdefault(m, []).append(v)

    median_months = {}
    for m in sorted(month_values.keys()):
        vals = sorted(month_values[m])
        mid = len(vals) // 2
        if len(vals) % 2 == 1:
            median = vals[mid]
        else:
            median = 0.5 * (vals[mid - 1] + vals[mid])
        median_months[m] = round(median, 3)

    remaining_months = sorted([a['remaining_months'] for a in agents])
    mid = len(remaining_months) // 2
    if len(remaining_months) % 2 == 1:
        median_remaining_months = remaining_months[mid]
    else:
        median_remaining_months = 0.5 * (remaining_months[mid - 1] + remaining_months[mid])

    median_remaining_years = max(0.0, median_remaining_months / 12.0)

    years = {}
    
    # Get the range of months that actually have data
    if median_months:
        min_month = min(median_months.keys())
        max_month = max(median_months.keys())
        
        # Calculate the year range based on actual data
        start_year = min_month // 12
        end_year = max_month // 12
        
        # Generate yearly aggregates for years that have data
        for y in range(start_year, end_year + 1):
            month_start = y * 12
            month_end = month_start + 11
            vals = [v for m, v in median_months.items() if month_start <= m <= month_end]
            years[y] = round(sum(vals) / len(vals), 3) if vals else None
    
    # Also create empty entries for years 0 through start_year-1 if needed for consistency
    if median_months:
        min_data_year = min_month // 12
        for y in range(0, min_data_year):
            years[y] = None

    time_series = {'months': median_months, 'year': years}

    est_remaining_service_life = ep_estimate_remaining_service_life(agents, facility, age_in_years)

    return Facility(
        facility=facility,
        age_in_years=age_in_years,
        condition_index=condition_index,
        time_series=time_series,
        estimated_remaining_service_life=est_remaining_service_life,
    )
