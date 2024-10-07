from fastapi import APIRouter
from pydantic import BaseModel
from ..models.answers import HouseholdEnergyProfileAnswers
from ..services.cost_calculator import calculate_savings, calculate_emissions_reduction

router = APIRouter()

class SavingsAndEmissionsResponse(BaseModel):
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
    average_household_savings: float = 1000  # Placeholder when no data is provided


@router.post("/household-energy-profile/")
def household_energy_profile(profile: HouseholdEnergyProfileAnswers):
    """
    Calculate savings and emissions reductions for the household energy profile.
    Returns:
    - Savings and emissions reductions for heating, hot water, cooking, and driving.
    """
    if not profile:
        return SavingsAndEmissionsResponse()

    # Calculate savings and emissions reduction for each section
    heating_savings = 0
    hot_water_savings = 0
    cooktop_savings = 0
    driving_savings = 0
    heating_emissions_reduction = 0
    hot_water_emissions_reduction = 0
    cooktop_emissions_reduction = 0
    driving_emissions_reduction = 0

    # Calculate heating savings and emissions reduction
    if profile.heating:
        heating_savings = calculate_savings(profile.heating, profile.your_home)
        heating_emissions_reduction = calculate_emissions_reduction(profile.heating, profile.your_home)

    # Calculate hot water savings and emissions reduction
    if profile.hot_water:
        hot_water_savings = calculate_savings(profile.hot_water, profile.your_home)
        hot_water_emissions_reduction = calculate_emissions_reduction(profile.hot_water, profile.your_home)

    # Calculate cooktop savings and emissions reduction
    if profile.cooktop:
        cooktop_savings = calculate_savings(profile.cooktop, profile.your_home)
        cooktop_emissions_reduction = calculate_emissions_reduction(profile.cooktop, profile.your_home)

    # Calculate driving savings and emissions reduction
    if profile.driving:
        driving_savings = calculate_savings(profile.driving, profile.your_home)
        driving_emissions_reduction = calculate_emissions_reduction(profile.driving, profile.your_home)

    # Aggregate the overall savings and emissions reduction
    overall_savings = heating_savings + hot_water_savings + cooktop_savings + driving_savings
    overall_emissions_reduction = (
        heating_emissions_reduction + hot_water_emissions_reduction + cooktop_emissions_reduction + driving_emissions_reduction
    ) / 4  # Average of the reductions

    response = SavingsAndEmissionsResponse(
        heating_savings=heating_savings,
        hot_water_savings=hot_water_savings,
        cooktop_savings=cooktop_savings,
        driving_savings=driving_savings,
        overall_savings=overall_savings,
        heating_emissions_reduction=heating_emissions_reduction,
        hot_water_emissions_reduction=hot_water_emissions_reduction,
        cooktop_emissions_reduction=cooktop_emissions_reduction,
        driving_emissions_reduction=driving_emissions_reduction,
        overall_emissions_reduction=overall_emissions_reduction
    )

    return {"success": True, "response": response}
