"""
Agent simulator (Eva Pavlik's version).
"""
import random

DEGRADED_THRESHOLD = 25.0
P = 99.999


def _simulate_agent(age_in_months, cond_index, facility, months_horizon, seed_offset):
    r = random.Random(seed_offset)
    base_monthly_rate = 1.0 / (facility.life_expectancy * 12.0 + 1.0)

    months = {}
    cond = cond_index
    remaining_months = None

    for m in range(age_in_months, age_in_months + months_horizon + 1):
        cond = cond * (1.0 - base_monthly_rate)

        if r.random() < 0.02:
            shock = r.uniform(5.0, 30.0)
            cond = max(1.0, cond - shock)

        cond += r.uniform(-0.3, 0.3)
        cond = max(1.0, min(99.999, cond))

        months[m] = round(cond, 3)

        if remaining_months is None and cond <= DEGRADED_THRESHOLD:
            remaining_months = m - age_in_months

    if remaining_months is None:
        remaining_months = max(0, (facility.life_expectancy * 12) - age_in_months)

    return {'months': months, 'remaining_months': remaining_months}


def ep_agent_simulator(age_in_months, condition_index, facility, n_agents=200, months_horizon=120, seed: int | None = None):
    agents = []
    base_seed = seed or random.randint(0, 2**31 - 1)
    for i in range(n_agents):
        seed_offset = base_seed + i * 100
        agent_res = _simulate_agent(age_in_months, condition_index, facility, months_horizon, seed_offset)
        agents.append(agent_res)
    return agents
