from ..models.energy_plans import ElectricityPlan, NaturalGasPlan, LPGPlan
from ..models.usage_profiles import HouseholdYearlyFuelUsageProfile

def get_default_electricity_plan():
    return ElectricityPlan(
        name="Basic Electricity Plan",
        nzd_per_day_kwh=0.20,
        nzd_per_night_kwh=0.18,
        nzd_per_controlled_kwh=0.15,
        daily_charge=1.25
    )

def get_default_natural_gas_plan():
    return NaturalGasPlan(
        name="Basic Natural Gas Plan",
        per_natural_gas_kwh=0.10,
        daily_charge=1.5
    )

def get_default_lpg_plan():
    return LPGPlan(
        name="Basic LPG Plan",
        per_lpg_kwh=0.25,
        daily_charge=80/365.25
    )

def get_default_usage_profile():
    return HouseholdYearlyFuelUsageProfile(
        elx_connection_days=365,
        day_kwh=2000,
        night_kwh=1000,
        controlled_kwh=500,
        natural_gas_connection_days=0,
        natural_gas_kwh=0,
        lpg_tank_rental_days=0,
        lpg_kwh=0
    )
