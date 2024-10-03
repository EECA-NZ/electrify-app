from .configuration import get_default_electricity_plan, get_default_natural_gas_plan, get_default_lpg_plan
from .energy_usage_estimator import estimate_usage_from_profile

def calculate_cost(plan, profile):
    # Placeholder for cost calculation based on plan type
    if isinstance(plan, ElectricityPlan):
        return (profile.day_kwh * plan.nzd_per_day_kwh +
                profile.night_kwh * plan.nzd_per_night_kwh +
                profile.controlled_kwh * plan.nzd_per_controlled_kwh +
                profile.elx_connection_days * plan.daily_charge)
    # Add similar calculations for other plan types

def find_lowest_cost(profiles, pricing_structures):
    min_cost = float('inf')
    best_plan = None
    best_profile = None
    for plan in pricing_structures:
        for profile in profiles:
            usage_profile = estimate_usage_from_profile(profile)
            cost = calculate_cost(plan, usage_profile)
            if cost < min_cost:
                min_cost = cost
                best_plan = plan
                best_profile = profile
    return min_cost, best_plan, best_profile

def find_lowest_cost(profiles, pricing_structures):
    min_cost = float('inf')
    best_plan = None
    best_profile = None
    for plan in pricing_structures:
        for profile in profiles:
            cost = plan.calculate_cost(profile)
            if cost < min_cost:
                min_cost = cost
                best_plan = plan
                best_profile = profile
    return min_cost, best_plan, best_profile

def find_biggest_savings(current_profile, possible_profiles, pricing_structures):
    max_savings = 0
    best_plan = None
    best_profile = None
    for plan in pricing_structures:
        current_cost = plan.calculate_cost(current_profile)
        for profile in possible_profiles:
            cost = plan.calculate_cost(profile)
            savings = current_cost - cost
            if savings > max_savings:
                max_savings = savings
                best_plan = plan
                best_profile = profile
    return max_savings, best_plan, best_profile