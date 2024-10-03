from app.models.answers import HouseholdEnergyProfileAnswers
from app.models.usage_profiles import HouseholdYearlyFuelUsageProfile

DAYS_IN_YEAR = 365.25

def uses_electricity(profile: HouseholdEnergyProfileAnswers) -> bool:
    return True

def uses_natural_gas(profile: HouseholdEnergyProfileAnswers) -> bool:
    if profile.heating.main_heating_source in ['Gas central heating', 'Gas heater']:
        return True
    if profile.hot_water.hot_water_heating_source in ['Gas hot water cylinder', 'Gas continuous hot water']:
        return True
    if profile.cooktop.cooktop == 'Gas hob':
        return True
    return False

def uses_lpg(profile: HouseholdEnergyProfileAnswers) -> bool:
    if profile.heating.main_heating_source == 'Bottled gas heater':
        return True
    if profile.hot_water.hot_water_heating_source in ['Gas hot water cylinder (bottled)', 'Gas continuous hot water (bottled)']:
        return True
    return False

def estimate_usage_from_profile(answers: HouseholdEnergyProfileAnswers) -> HouseholdYearlyFuelUsageProfile:
    your_home = answers.your_home
    heating = answers.heating
    hot_water = answers.hot_water
    cooktop = answers.cooktop
    driving = answers.driving
    solar = answers.solar

    heating_profile = heating.energy_usage_pattern(your_home, solar)
    hot_water_profile = hot_water.energy_usage_pattern(your_home, solar)
    cooktop_profile = cooktop.energy_usage_pattern(your_home, solar)
    driving_profile = driving.energy_usage_pattern(your_home, solar)

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
    day_kwh = heating_profile.day_kwh + hot_water_profile.day_kwh + cooktop_profile.day_kwh + driving_profile.day_kwh
    night_kwh = heating_profile.night_kwh + hot_water_profile.night_kwh + cooktop_profile.night_kwh + driving_profile.night_kwh
    controlled_kwh = heating_profile.controlled_kwh + hot_water_profile.controlled_kwh + cooktop_profile.controlled_kwh + driving_profile.controlled_kwh

    # Natural gas and LPG
    natural_gas_kwh = heating_profile.natural_gas_kwh + hot_water_profile.natural_gas_kwh + cooktop_profile.natural_gas_kwh
    lpg_kwh = heating_profile.lpg_kwh + hot_water_profile.lpg_kwh + cooktop_profile.lpg_kwh

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
        diesel_litres=driving_profile.diesel_litres
    )
