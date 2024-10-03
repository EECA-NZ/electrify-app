from ..models.energy_plans import ElectricityPlan, NaturalGasPlan, LPGPlan
from ..models.usage_profiles import HouseholdYearlyFuelUsageProfile
from ..models.answers import YourHomeAnswers, HeatingAnswers, HotWaterAnswers, CooktopAnswers, DrivingAnswers, SolarAnswers

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
        lpg_kwh=0,
        petrol_litres=1000,
        diesel_litres=0,
    )

def get_default_your_home_answers():
    return YourHomeAnswers(
        people_in_house=4,
        postcode='0000'
    )

def get_default_heating_answers():
    return HeatingAnswers(
        main_heating_source='Heat pump',
        heating_during_day='Yes',
        insulation_quality='Somewhere in between'
    )

def get_default_hot_water_answers():
    return HotWaterAnswers(
        hot_water_usage='Medium',
        hot_water_heating_source='Electric hot water cylinder'
    )

def get_default_cooktop_answers():
    return CooktopAnswers(
        cooktop='Electric'
    )

def get_default_driving_answers():
    return DrivingAnswers(
        vehicle='ICE',
        usage='Medium'
    )

def get_default_solar_answers():
    return SolarAnswers(
        arraySizekW=0.0,
        inverterSizekW=0.0
    )

def get_default_household_energy_profile():
    return {
        "your_home": get_default_your_home_answers(),
        "heating": get_default_heating_answers(),
        "hot_water": get_default_hot_water_answers(),
        "cooktop": get_default_cooktop_answers(),
        "driving": get_default_driving_answers(),
        "solar": get_default_solar_answers(),
        "usage_profile": get_default_usage_profile()
    }
