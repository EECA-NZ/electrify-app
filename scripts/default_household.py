"""
This script illustrates how to use a household's answers to calculate
a household energy use profile. It then constructs an energy plan and
calculates the total annual cost of energy for the household.
"""

from app.models.energy_plans import HouseholdEnergyPlan
from app.models.answers import HouseholdEnergyProfileAnswers
from app.services.energy_usage_estimator import estimate_usage_from_profile
import app.services.configuration as cfg

household_profile = HouseholdEnergyProfileAnswers(
    your_home=cfg.get_default_your_home_answers(),
    heating=cfg.get_default_heating_answers(),
    hot_water=cfg.get_default_hot_water_answers(),
    cooktop=cfg.get_default_cooktop_answers(),
    driving=cfg.get_default_driving_answers(),
    solar=cfg.get_default_solar_answers()
)

my_plan = HouseholdEnergyPlan(
    name="Basic Household Energy Plan",
    electricity_plan=cfg.get_default_electricity_plan(),
    natural_gas_plan=cfg.get_default_natural_gas_plan(),
    lpg_plan=cfg.get_default_lpg_plan()
)

household_energy_use = estimate_usage_from_profile(household_profile)
total_energy_costs = my_plan.calculate_cost(household_energy_use)

print(household_profile)
print(household_energy_use)
print("total cost: ", total_energy_costs)
