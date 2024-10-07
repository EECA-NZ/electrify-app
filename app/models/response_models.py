"""
Module for endpoint response objects
"""

from pydantic import BaseModel


class SavingsAndEmissionsResponse(BaseModel):
    """
    Response model for the household energy profile endpoint.
    """

    heating_savings: float = 0
    hot_water_savings: float = 0
    cooktop_savings: float = 0
    driving_savings: float = 0
    overall_savings: float = 0
    heating_emissions_reduction: float = 0
    hot_water_emissions_reduction: float = 0
    cooktop_emissions_reduction: float = 0
    driving_emissions_reduction: float = 0
    overall_emissions_reduction: float = 0
    average_household_savings: float = 1000
