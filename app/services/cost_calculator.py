"""
This module provides functions to optimize the cost of energy for a household.
"""

from .energy_usage_estimator import estimate_usage_from_profile

def find_lowest_cost(profiles, pricing_structures):
    """
    Find the lowest cost energy plan for a household

    Args:
    profiles: list of HouseholdEnergyProfileAnswers objects
    pricing_structures: list of HouseholdEnergyPlan objects

    Returns:
    min_cost: float, the lowest cost found
    """
    min_cost = float('inf')
    best_plan = None
    best_profile = None
    for plan in pricing_structures:
        for profile in profiles:
            usage_profile = estimate_usage_from_profile(profile)
            cost = plan.calculate_cost(usage_profile)
            if cost < min_cost:
                min_cost = cost
                best_plan = plan
                best_profile = profile
    return min_cost, best_plan, best_profile

def find_biggest_savings(current_profile, possible_profiles, pricing_structures):
    """
    Find the biggest savings possible for a household

    Args:
    current_profile: HouseholdEnergyProfileAnswers object
    possible_profiles: list of HouseholdEnergyProfileAnswers objects
    pricing_structures: list of HouseholdEnergyPlan objects

    Returns:
    max_savings: float, the biggest savings found
    best_plan: HouseholdEnergyPlan object, the best plan found
    best_profile: HouseholdEnergyProfileAnswers object, the best
    profile found
    """
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

# pylint: disable=unused-argument
def calculate_savings(answers, your_home):
    """
    Placeholder function to calculate dollar savings based on user input.
    This could use factors such as current fuel cost, energy use, etc.
    """
    return 100  # Placeholder for actual savings calculation logic

def calculate_emissions_reduction(answers, your_home):
    """
    Placeholder function to calculate percentage emissions reduction based on user input.
    """
    return 20  # Placeholder for actual emissions reduction logic
