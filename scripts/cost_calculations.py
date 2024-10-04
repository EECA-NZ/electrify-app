"""
This script illustrates how to use a household's energy usage profile
to calculate the total annual cost of energy for the household.
"""

from app.models.energy_plans import HouseholdEnergyPlan

import app.services.configuration as cfg

my_plan = HouseholdEnergyPlan(
    name="Basic Household Energy Plan",
    electricity_plan=cfg.get_default_electricity_plan(),
    natural_gas_plan=cfg.get_default_natural_gas_plan(),
    lpg_plan=cfg.get_default_lpg_plan()
)

my_profile = cfg.get_default_usage_profile()

print(my_plan.calculate_cost(my_profile))
