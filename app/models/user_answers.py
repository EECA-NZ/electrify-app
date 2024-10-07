"""
Classes for storing user answers to the questions provided by online users.
"""

from typing import Literal, Optional
from pydantic import BaseModel, constr, conint
from .usage_profiles import (
    HeatingYearlyFuelUsageProfile,
    HotWaterYearlyFuelUsageProfile,
    CooktopYearlyFuelUsageProfile,
    DrivingYearlyFuelUsageProfile,
    SolarYearlyFuelGenerationProfile,
)
from ..services import get_climate_zone
from ..constants import DAYS_IN_YEAR, AVERAGE_HOUSEHOLD_SIZE, SOLAR_RESOURCE_KWH_PER_DAY


class YourHomeAnswers(BaseModel):
    """
    Answers to questions about the user's home.
    """

    people_in_house: conint(ge=1, le=6)
    postcode: constr(strip_whitespace=True, pattern=r"^\d{4}$")


class HeatingAnswers(BaseModel):
    """
    Answers to questions about the user's space heating.
    """

    main_heating_source: Literal[
        "Piped gas heater",
        "Bottled gas heater",
        "Heat pump",
        "Heat pump (ducted)",
        "Electric heater",
        "Wood burner",
    ]
    alternative_main_heating_source: Literal[
        "Piped gas heater",
        "Bottled gas heater",
        "Heat pump",
        "Heat pump (ducted)",
        "Electric heater",
        "Wood burner",
    ]
    heating_during_day: Literal[
        "Never",
        "1-2 days a week",
        "3-4 days a week",
        "5-7 days a week",
    ]
    insulation_quality: Literal[
        "Not well insulated", "Moderately insulated", "Well insulated"
    ]

    def energy_usage_pattern(
        self, your_home, use_alternative: bool = False
    ) -> HeatingYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for space heating.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.

        Returns
        -------
        HeatingYearlyFuelUsageProfile
            The yearly fuel usage profile for space heating.
        """
        main_heating_source = (
            self.alternative_main_heating_source
            if use_alternative
            else self.main_heating_source
        )
        total_kwh = {"Piped gas heater": 3000}.get(
            main_heating_source, 0
        ) * your_home.people_in_house
        return HeatingYearlyFuelUsageProfile(
            elx_connection_days=365,
            day_kwh=total_kwh,
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

    hot_water_usage: Literal["Low", "Average", "High"]
    hot_water_heating_source: Literal[
        "Electric hot water cylinder",
        "Piped gas hot water cylinder",
        "Piped gas instantaneous",
        "Bottled gas instantaneous",
        "Hot water heat pump",
    ]
    alternative_hot_water_heating_source: Literal[
        "Electric hot water cylinder",
        "Piped gas hot water cylinder",
        "Piped gas instantaneous",
        "Bottled gas instantaneous",
        "Hot water heat pump",
    ]

    def energy_usage_pattern(
        self, your_home, use_alternative: bool = True
    ) -> HotWaterYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for hot water heating.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.

        Returns
        -------
        HotWaterYearlyFuelUsageProfile
            The yearly fuel usage profile for hot water heating.
        """
        hot_water_heating_source = (
            self.alternative_hot_water_heating_source
            if use_alternative
            else self.hot_water_heating_source
        )
        total_kwh = {"Hot water heat pump": 3000}.get(
            hot_water_heating_source, 0
        ) * your_home.people_in_house
        day_night = {"Low": (0.6, 0.4), "Average": (0.7, 0.3), "High": (0.8, 0.2)}
        day_kwh = total_kwh * day_night[self.hot_water_usage][0]
        night_kwh = total_kwh * day_night[self.hot_water_usage][1]
        return HotWaterYearlyFuelUsageProfile(
            elx_connection_days=365,
            day_kwh=day_kwh,
            night_kwh=night_kwh,
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
    alternative_cooktop: Literal[
        "Electric induction", "Piped gas", "Bottled gas", "Electric (coil or ceramic)"
    ]

    def energy_usage_pattern(
        self, your_home, use_alternative: bool = False
    ) -> CooktopYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for cooking.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.

        Returns
        -------
        CooktopYearlyFuelUsageProfile
            The yearly fuel usage profile for cooking.
        """
        usage_factors = {
            "Electric induction": {
                "standard_household_kwh": 294,
                "elx_connection_days": DAYS_IN_YEAR,
            },
            "Electric (coil or ceramic)": {
                "standard_household_kwh": 325,
                "elx_connection_days": DAYS_IN_YEAR,
            },
            "Piped gas": {
                "standard_household_kwh": 760,
                "natural_gas_connection_days": DAYS_IN_YEAR,
            },
            "Bottled gas": {
                "standard_household_kwh": 760,
                "lpg_tank_rental_days": 2 * DAYS_IN_YEAR,
            },
        }
        cooktop_type = self.alternative_cooktop if use_alternative else self.cooktop
        if cooktop_type not in usage_factors:
            raise ValueError(f"Unknown cooktop type: {cooktop_type}")

        factor = usage_factors[cooktop_type]
        total_kwh = (
            factor["standard_household_kwh"]
            * (1 + your_home.people_in_house)
            / (1 + AVERAGE_HOUSEHOLD_SIZE)
        )

        return CooktopYearlyFuelUsageProfile(
            elx_connection_days=factor.get("elx_connection_days", 0),
            day_kwh=total_kwh if "Electric" in cooktop_type else 0,
            night_kwh=0,
            controlled_kwh=0,
            natural_gas_connection_days=factor.get("natural_gas_connection_days", 0),
            natural_gas_kwh=total_kwh if cooktop_type == "Piped gas" else 0,
            lpg_tank_rental_days=factor.get("lpg_tank_rental_days", 0),
            lpg_kwh=total_kwh if cooktop_type == "Bottled gas" else 0,
            petrol_litres=0,
            diesel_litres=0,
        )


class DrivingAnswers(BaseModel):
    """
    Answers to questions about the user's vehicle and driving patterns.
    """

    vehicle_type: Literal["Petrol", "Diesel", "Hybrid", "Plug-in hybrid", "Electric"]
    alternative_vehicle_type: Literal[
        "Petrol", "Diesel", "Hybrid", "Plug-in hybrid", "Electric"
    ]
    vehicle_size: Literal["Small", "Medium", "Large"]
    km_per_week: Literal["50 or less", "100", "200", "300", "400 or more"]

    def energy_usage_pattern(
        self, your_home, use_alternative: bool = False
    ) -> DrivingYearlyFuelUsageProfile:
        """
        Return the yearly fuel usage profile for driving.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.

        Returns
        -------
        DrivingYearlyFuelUsageProfile
            The yearly fuel usage profile for driving.
        """
        vehicle_type = (
            self.alternative_vehicle_type if use_alternative else self.vehicle_type
        )
        petrol_usage = {"Petrol": 1000}.get(vehicle_type, 0) * your_home.people_in_house
        return DrivingYearlyFuelUsageProfile(
            elx_connection_days=0,
            day_kwh=0,
            night_kwh=0,
            controlled_kwh=0,
            natural_gas_connection_days=0,
            natural_gas_kwh=0,
            lpg_tank_rental_days=0,
            lpg_kwh=0,
            petrol_litres=petrol_usage,
            diesel_litres=0,
        )


class SolarAnswers(BaseModel):
    """
    Does the house include solar panels?
    """

    hasSolar: bool

    def energy_generation(self, your_home) -> SolarYearlyFuelGenerationProfile:
        """
        Return the yearly energy generation profile for solar energy generation.

        The profile is based on the answers provided by the user.

        Parameters
        ----------
        your_home : YourHomeAnswers
            Answers to questions about the user's home.

        Returns
        -------
        SolarYearlyFuelUsageProfile
            The yearly fuel usage profile for solar energy generation.
        """
        my_climate_zone = get_climate_zone.climate_zone(your_home.postcode)
        annual_generation_kwh = 0
        if self.hasSolar:
            annual_generation_kwh = (
                SOLAR_RESOURCE_KWH_PER_DAY[my_climate_zone] * DAYS_IN_YEAR
            )

        return SolarYearlyFuelGenerationProfile(
            elx_connection_days=0,
            day_kwh=-annual_generation_kwh,
            night_kwh=0,
            controlled_kwh=0,
            natural_gas_connection_days=0,
            natural_gas_kwh=0,
            lpg_tank_rental_days=0,
            lpg_kwh=0,
            petrol_litres=0,
            diesel_litres=0,
        )


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
