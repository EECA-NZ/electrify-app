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