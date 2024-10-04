"""
Configuration functions including default values for energy plans, usage profiles, and answers.
"""

from ..models.energy_plans import ElectricityPlan, NaturalGasPlan, LPGPlan
from ..models.usage_profiles import HouseholdYearlyFuelUsageProfile
from ..models.answers import YourHomeAnswers, HeatingAnswers
from ..models.answers import HotWaterAnswers, CooktopAnswers
from ..models.answers import DrivingAnswers, SolarAnswers


def get_default_electricity_plan():
    """
    Return a default electricity plan.
    """
    return ElectricityPlan(
        name="Basic Electricity Plan",
        nzd_per_day_kwh=0.20,
        nzd_per_night_kwh=0.18,
        nzd_per_controlled_kwh=0.15,
        daily_charge=1.25
    )

def get_default_natural_gas_plan():
    """
    Return a default natural gas plan.
    """
    return NaturalGasPlan(
        name="Basic Natural Gas Plan",
        per_natural_gas_kwh=0.10,
        daily_charge=1.5
    )

def get_default_lpg_plan():
    """
    Return a default LPG plan.
    """
    return LPGPlan(
        name="Basic LPG Plan",
        per_lpg_kwh=0.25,
        daily_charge=80/365.25
    )

def get_default_usage_profile():
    """
    Return a default energy usage profile.
    """
    return HouseholdYearlyFuelUsageProfile(
        elx_connection_days=365,
        day_kwh=2000,
        night_kwh=1000,
        controlled_kwh=500,
        natural_gas_connection_days=0,
        natural_gas_kwh=0,
        lpg_tank_rental_days=0,
        lpg_kwh=0,
        petrol_litres=1000,
        diesel_litres=0,
    )

def get_default_your_home_answers():
    """
    Return a default 'your home' answers object.
    """
    return YourHomeAnswers(
        people_in_house=4,
        postcode='0000'
    )

def get_default_heating_answers():
    """
    Return a default 'heating' answers object.
    """
    return HeatingAnswers(
        main_heating_source='Heat pump',
        heating_during_day='Yes',
        insulation_quality='Somewhere in between'
    )

def get_default_hot_water_answers():
    """
    Return a default 'hot water' answers object.
    """
    return HotWaterAnswers(
        hot_water_usage='Medium',
        hot_water_heating_source='Electric hot water cylinder'
    )

def get_default_cooktop_answers():
    """
    Return a default 'cooktop' answers object.
    """
    return CooktopAnswers(
        cooktop='Electric (coil or ceramic)'
    )

def get_default_driving_answers():
    """
    Return a default 'driving' answers object.
    """
    return DrivingAnswers(
        vehicle='ICE',
        usage='Medium'
    )

def get_default_solar_answers():
    """
    Return a default 'solar' answers object.
    """
    return SolarAnswers(
        arraySizekW=0.0,
        inverterSizekW=0.0
    )

def get_default_household_energy_profile():
    """
    Return a default overall household answers object.
    """
    return {
        "your_home": get_default_your_home_answers(),
        "heating": get_default_heating_answers(),
        "hot_water": get_default_hot_water_answers(),
        "cooktop": get_default_cooktop_answers(),
        "driving": get_default_driving_answers(),
        "solar": get_default_solar_answers(),
        "usage_profile": get_default_usage_profile()
    }
