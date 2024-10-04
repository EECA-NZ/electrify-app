"""
Classes for storing user answers to the questions provided by online users.
"""

from typing import Literal, Optional
from pydantic import BaseModel, constr, conint, confloat
from .usage_profiles import (
    HeatingYearlyFuelUsageProfile,
    HotWaterYearlyFuelUsageProfile,
    CooktopYearlyFuelUsageProfile,
    DrivingYearlyFuelUsageProfile,
)

DAYS_IN_YEAR = 365.25

class YourHomeAnswers(BaseModel):
    """
    Answers to questions about the user's home.
    """
    people_in_house: conint(ge=1)
    postcode: constr(strip_whitespace=True, pattern=r"^\d{4}$")


class HeatingAnswers(BaseModel):
    """
    Answers to questions about the user's space heating.
    """
    main_heating_source: Literal[
        "Electric heater",
        "Wood burner",
        "Heat pump",
        "Bottled gas heater",
        "Gas central heating",
        "Gas heater",
        "Coal range",
        "Heat Pump (ducted)",
    ]
    heating_during_day: Literal["Yes", "No"]
    insulation_quality: Literal[
        "Not well insulated", "Somewhere in between", "Well insulated"
    ]

    def energy_usage_pattern(self, your_home, solar) -> HeatingYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for space heating.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.
        solar : SolarAnswers
            Answers to questions about the user's solar panels.

        Returns
        -------
        HeatingYearlyFuelUsageProfile
            The yearly fuel usage profile for space heating.
        """
        has_solar = solar.arraySizekW > 0
        if has_solar:
            has_solar = 1000 * min(solar.arraySize, solar.inverterSize)
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
            diesel_litres=0,
        )


class HotWaterAnswers(BaseModel):
    """
    Answers to questions about the user's hot water heating.
    """
    hot_water_usage: Literal["Low", "Medium", "High"]
    hot_water_heating_source: Literal[
        "Gas hot water cylinder",
        "Gas continuous hot water",
        "Electric hot water cylinder",
        "Electric continuous hot water",
        "Hot water heat pump",
        "Wetback",
        "Solar hot water",
        "No hot water",
        "Unsure",
    ]

    def energy_usage_pattern(self, your_home, solar) -> HotWaterYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for hot water heating.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.
        solar : SolarAnswers
            Answers to questions about the user's solar panels.

        Returns
        -------
        HotWaterYearlyFuelUsageProfile
            The yearly fuel usage profile for hot water heating.
        """
        has_solar = solar.arraySizekW > 0
        if has_solar:
            has_solar = 1000 * min(solar.arraySize, solar.inverterSize)
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
            diesel_litres=0,
        )


class CooktopAnswers(BaseModel):
    """
    Answers to questions about the user's stove.
    """
    cooktop: Literal[
        "Electric induction", "Piped gas", "Bottled gas", "Electric (coil or ceramic)"
    ]

    def energy_usage_pattern(self, your_home, solar) -> CooktopYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for cooking.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.
        solar : SolarAnswers
            Answers to questions about the user's solar panels.

        Returns
        -------
        CooktopYearlyFuelUsageProfile
            The yearly fuel usage profile for cooking.
        """
        has_solar = solar.arraySizekW > 0
        if has_solar:
            has_solar = 1000 * min(solar.arraySize, solar.inverterSize)
        if self.cooktop == 'Electric induction':
            total_kwh = 159 * 0.5 * (1 + your_home.people_in_house)
            # All electricity use is during the day
            return CooktopYearlyFuelUsageProfile(
                elx_connection_days=365,
                day_kwh=total_kwh,
                night_kwh=0,
                controlled_kwh=0,
                natural_gas_connection_days=0,
                natural_gas_kwh=0,
                lpg_tank_rental_days=0,
                lpg_kwh=0,
                petrol_litres=0,
                diesel_litres=0,
            )
        if self.cooktop == 'Electric (coil or ceramic)':
            total_kwh = 176 * 0.5 * (1 + your_home.people_in_house)
            # All electricity use is during the day
            return CooktopYearlyFuelUsageProfile(
                elx_connection_days=365,
                day_kwh=total_kwh,
                night_kwh=0,
                controlled_kwh=0,
                natural_gas_connection_days=0,
                natural_gas_kwh=0,
                lpg_tank_rental_days=0,
                lpg_kwh=0,
                petrol_litres=0,
                diesel_litres=0,
            )
        if self.cooktop == 'Piped gas':
            total_kwh = 412 * 0.5 * (1 + your_home.people_in_house)
            return CooktopYearlyFuelUsageProfile(
                elx_connection_days=365,
                day_kwh=0,
                night_kwh=0,
                controlled_kwh=0,
                natural_gas_connection_days=0,
                natural_gas_kwh=total_kwh,
                lpg_tank_rental_days=0,
                lpg_kwh=0,
                petrol_litres=0,
                diesel_litres=0,
            )
        if self.cooktop == 'Bottled gas':
            total_kwh = 412 * 0.5 * (1 + your_home.people_in_house)
            return CooktopYearlyFuelUsageProfile(
                elx_connection_days=365,
                day_kwh=0,
                night_kwh=0,
                controlled_kwh=0,
                natural_gas_connection_days=0,
                natural_gas_kwh=0,
                lpg_tank_rental_days=2 * DAYS_IN_YEAR,
                lpg_kwh=total_kwh,
                petrol_litres=0,
                diesel_litres=0,
            )
        raise ValueError(f"Unknown cooktop type: {self.cooktop}")


class DrivingAnswers(BaseModel):
    """
    Answers to questions about the user's vehicle and driving patterns.
    """
    vehicle: Literal["EV", "ICE"]
    usage: Literal["Low", "Medium", "High"]

    def energy_usage_pattern(self, your_home, solar) -> DrivingYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for driving.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.
        solar : SolarAnswers
            Answers to questions about the user's solar panels.

        Returns
        -------
        DrivingYearlyFuelUsageProfile
            The yearly fuel usage profile for driving.
        """
        has_solar = solar.arraySizekW > 0
        if has_solar:
            has_solar = 1000 * min(solar.arraySize, solar.inverterSize)
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
            diesel_litres=0,
        )


class SolarAnswers(BaseModel):
    """
    Does the house include solar panels?
    """
    arraySizekW: confloat(ge=0)
    inverterSizekW: confloat(ge=0)


class HouseholdEnergyProfileAnswers(BaseModel):
    """
    Answers to all questions about the user's household energy usage.

    This class is used to store all the answers provided by the user.
    """
    your_home: Optional[YourHomeAnswers] = None
    heating: Optional[HeatingAnswers] = None
    hot_water: Optional[HotWaterAnswers] = None
    cooktop: Optional[CooktopAnswers] = None
    driving: Optional[DrivingAnswers] = None
    solar: Optional[SolarAnswers] = None
