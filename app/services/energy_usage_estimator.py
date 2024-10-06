"""
This module provides functions to estimate a household's yearly fuel usage profile.
"""

# pylint: disable=too-many-locals

from app.models.answers import HouseholdEnergyProfileAnswers
from app.models.usage_profiles import HouseholdYearlyFuelUsageProfile, YearlyFuelUsageProfile
from app.constants import DAYS_IN_YEAR, EMISSIONS_FACTORS


def uses_electricity(profile: HouseholdEnergyProfileAnswers) -> bool:
    """
    Return True if the household uses electricity.
    """
    return profile is not None


def uses_natural_gas(profile: HouseholdEnergyProfileAnswers) -> bool:
    """
    Return True if the household uses natural gas.
    """
    if profile.heating.main_heating_source in ["Gas central heating", "Gas heater"]:
        return True
    if profile.hot_water.hot_water_heating_source in [
        "Gas hot water cylinder",
        "Gas continuous hot water",
    ]:
        return True
    if profile.cooktop.cooktop == "Gas hob":
        return True
    return False


def uses_lpg(profile: HouseholdEnergyProfileAnswers) -> bool:
    """
    Return True if the household uses LPG.
    """
    if profile.heating.main_heating_source == "Bottled gas heater":
        return True
    if profile.hot_water.hot_water_heating_source in [
        "Gas hot water cylinder (bottled)",
        "Gas continuous hot water (bottled)",
    ]:
        return True
    return False


def estimate_usage_from_profile(
    answers: HouseholdEnergyProfileAnswers,
) -> HouseholdYearlyFuelUsageProfile:
    """
    Estimate the household's yearly fuel usage profile.
    """
    your_home = answers.your_home
    heating = answers.heating
    hot_water = answers.hot_water
    cooktop = answers.cooktop
    driving = answers.driving
    solar = answers.solar

    heating_profile = heating.energy_usage_pattern(your_home)
    hot_water_profile = hot_water.energy_usage_pattern(your_home)
    cooktop_profile = cooktop.energy_usage_pattern(your_home)
    driving_profile = driving.energy_usage_pattern(your_home)
    # pylint: disable=unused-variable
    solar_profile = solar.energy_generation(your_home)

    # Determine fixed charges
    elx_connection_days = 0
    lpg_tank_rental_days = 0
    natural_gas_connection_days = 0
    if uses_electricity(answers):
        elx_connection_days = DAYS_IN_YEAR
    if uses_lpg(answers):
        lpg_tank_rental_days = 2 * DAYS_IN_YEAR
    if uses_natural_gas(answers):
        natural_gas_connection_days = DAYS_IN_YEAR

    # Variable electricity
    day_kwh = (
        heating_profile.day_kwh
        + hot_water_profile.day_kwh
        + cooktop_profile.day_kwh
        + driving_profile.day_kwh
    )
    night_kwh = (
        heating_profile.night_kwh
        + hot_water_profile.night_kwh
        + cooktop_profile.night_kwh
        + driving_profile.night_kwh
    )
    controlled_kwh = (
        heating_profile.controlled_kwh
        + hot_water_profile.controlled_kwh
        + cooktop_profile.controlled_kwh
        + driving_profile.controlled_kwh
    )

    # Natural gas and LPG
    natural_gas_kwh = (
        heating_profile.natural_gas_kwh
        + hot_water_profile.natural_gas_kwh
        + cooktop_profile.natural_gas_kwh
    )
    lpg_kwh = (
        heating_profile.lpg_kwh + hot_water_profile.lpg_kwh + cooktop_profile.lpg_kwh
    )

    return HouseholdYearlyFuelUsageProfile(
        elx_connection_days=elx_connection_days,
        day_kwh=day_kwh,
        night_kwh=night_kwh,
        controlled_kwh=controlled_kwh,
        natural_gas_connection_days=natural_gas_connection_days,
        natural_gas_kwh=natural_gas_kwh,
        lpg_tank_rental_days=lpg_tank_rental_days,
        lpg_kwh=lpg_kwh,
        petrol_litres=driving_profile.petrol_litres,
        diesel_litres=driving_profile.diesel_litres,
    )


def emissions(usage_profile: YearlyFuelUsageProfile) -> float:
    """
    Return the household's yearly CO2 emissions in kg.
    """
    # List of emissions components
    components = [
        (usage_profile.day_kwh, "electricity"),
        (usage_profile.night_kwh, "electricity"),
        (usage_profile.controlled_kwh, "electricity"),
        (usage_profile.natural_gas_kwh, "natural_gas"),
        (usage_profile.lpg_kwh, "lpg"),
        (usage_profile.petrol_litres, "petrol"),
        (usage_profile.diesel_litres, "diesel"),
    ]

    # Calculate emissions with a default of 0 if the emission factor is missing
    total_emissions = sum(
        usage * EMISSIONS_FACTORS.get(fuel_type, 0) for usage, fuel_type in components
    )

    return total_emissions
