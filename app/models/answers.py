from typing import Literal, Optional
from pydantic import BaseModel, constr, conint, confloat
from .usage_profiles import HeatingYearlyFuelUsageProfile, HotWaterYearlyFuelUsageProfile, CooktopYearlyFuelUsageProfile, DrivingYearlyFuelUsageProfile

class YourHomeAnswers(BaseModel):
    people_in_house: conint(ge=1)
    postcode: constr(strip_whitespace=True,
                     pattern=r'^\d{4}$')

class HeatingAnswers(BaseModel):
    main_heating_source: Literal[
        'Electric heater',
        'Wood burner',
        'Heat pump',
        'Bottled gas heater',
        'Gas central heating',
        'Gas heater',
        'Coal range',
        'Heat Pump (ducted)'
    ]
    heating_during_day: Literal['Yes', 'No']
    insulation_quality: Literal[
        'Not well insulated',
        'Somewhere in between',
        'Well insulated']

    def energy_usage_pattern(self, your_home, solar) -> HeatingYearlyFuelUsageProfile:
        has_solar = solar.arraySizekW > 0
        if has_solar:
            total_electricity_usage -= 1000 * min(solar.arraySize, solar.inverterSize)
        return HeatingYearlyFuelUsageProfile(
            elx_connection_days=365,
            day_kwh=1000 * your_home.people_in_house,
            night_kwh=300,
            controlled_kwh=200,
            natural_gas_connection_days=0,
            natural_gas_kwh=0,
            lpg_tank_rental_days=0,
            lpg_kwh=0,
            petrol_litres=0,
            diesel_litres=0
        )

class HotWaterAnswers(BaseModel):
    hot_water_usage: Literal['Low', 'Medium', 'High']
    hot_water_heating_source: Literal[
        'Gas hot water cylinder',
        'Gas continuous hot water',
        'Electric hot water cylinder',
        'Electric continuous hot water',
        'Hot water heat pump',
        'Wetback',
        'Solar hot water',
        'No hot water',
        'Unsure'
    ]

    def energy_usage_pattern(self, your_home, solar) -> HotWaterYearlyFuelUsageProfile:
        has_solar = solar.arraySizekW > 0
        if has_solar:
            total_electricity_usage -= 1000 * min(solar.arraySize, solar.inverterSize)
        return HotWaterYearlyFuelUsageProfile(
            elx_connection_days=365,
            day_kwh=1000 * your_home.people_in_house,
            night_kwh=300,
            controlled_kwh=200,
            natural_gas_connection_days=0,
            natural_gas_kwh=0,
            lpg_tank_rental_days=0,
            lpg_kwh=0,
            petrol_litres=0,
            diesel_litres=0
        )

class CooktopAnswers(BaseModel):
    cooktop: Literal[
        'Electric induction',
        'Gas hob',
        'Electric']

    def energy_usage_pattern(self, your_home, solar) -> CooktopYearlyFuelUsageProfile:
        has_solar = solar.arraySizekW > 0
        if has_solar:
            total_electricity_usage -= 1000 * min(solar.arraySize, solar.inverterSize)
        return CooktopYearlyFuelUsageProfile(
            elx_connection_days=365,
            day_kwh=1000 * your_home.people_in_house,
            night_kwh=300,
            controlled_kwh=200,
            natural_gas_connection_days=0,
            natural_gas_kwh=0,
            lpg_tank_rental_days=0,
            lpg_kwh=0,
            petrol_litres=0,
            diesel_litres=0
        )

class DrivingAnswers(BaseModel):
    vehicle: Literal[
        'EV',
        'ICE'
    ]
    usage: Literal[
        'Low',
        'Medium',
        'High'
    ]

    def energy_usage_pattern(self, your_home, solar) -> DrivingYearlyFuelUsageProfile:
        has_solar = solar.arraySizekW > 0
        if has_solar:
            total_electricity_usage -= 1000 * min(solar.arraySize, solar.inverterSize)
        return DrivingYearlyFuelUsageProfile(
            elx_connection_days=0,
            day_kwh=0,
            night_kwh=0,
            controlled_kwh=0,
            natural_gas_connection_days=0,
            natural_gas_kwh=0,
            lpg_tank_rental_days=0,
            lpg_kwh=0,
            petrol_litres=1000 * your_home.people_in_house,
            diesel_litres=0
        )

class SolarAnswers(BaseModel):
    arraySizekW: confloat(ge=0)
    inverterSizekW: confloat(ge=0)

class HouseholdEnergyProfileAnswers(BaseModel):
    your_home: Optional[YourHomeAnswers] = None
    heating: Optional[HeatingAnswers] = None
    hot_water: Optional[HotWaterAnswers] = None
    cooktop: Optional[CooktopAnswers] = None
    driving: Optional[DrivingAnswers] = None
    solar: Optional[SolarAnswers] = None