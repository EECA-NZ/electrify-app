"""
Classes representing yearly fuel usage profiles for different household areas.
For simplicity they all have the same components even though some of them
might not be relevant for some areas.
"""

from pydantic import BaseModel


class HeatingYearlyFuelUsageProfile(BaseModel):
    """
    Space heating yearly fuel usage profile.
    """
    elx_connection_days: float
    day_kwh: float
    night_kwh: float
    controlled_kwh: float
    natural_gas_connection_days: int
    natural_gas_kwh: float
    lpg_tank_rental_days: float
    lpg_kwh: float
    petrol_litres: float
    diesel_litres: float


class HotWaterYearlyFuelUsageProfile(BaseModel):
    """
    Hot water yearly fuel usage profile.
    """
    elx_connection_days: float
    day_kwh: float
    night_kwh: float
    controlled_kwh: float
    natural_gas_connection_days: int
    natural_gas_kwh: float
    lpg_tank_rental_days: float
    lpg_kwh: float
    petrol_litres: float
    diesel_litres: float


class CooktopYearlyFuelUsageProfile(BaseModel):
    """
    Cooktop yearly fuel usage profile.
    """
    elx_connection_days: float
    day_kwh: float
    night_kwh: float
    controlled_kwh: float
    natural_gas_connection_days: int
    natural_gas_kwh: float
    lpg_tank_rental_days: float
    lpg_kwh: float
    petrol_litres: float
    diesel_litres: float


class DrivingYearlyFuelUsageProfile(BaseModel):
    """
    Driving yearly fuel usage profile.
    """
    elx_connection_days: float
    day_kwh: float
    night_kwh: float
    controlled_kwh: float
    natural_gas_connection_days: int
    natural_gas_kwh: float
    lpg_tank_rental_days: float
    lpg_kwh: float
    petrol_litres: float
    diesel_litres: float


class HouseholdYearlyFuelUsageProfile(BaseModel):
    """
    Overall household yearly fuel usage profile.
    """
    elx_connection_days: float
    day_kwh: float
    night_kwh: float
    controlled_kwh: float
    natural_gas_connection_days: int
    natural_gas_kwh: float
    lpg_tank_rental_days: float
    lpg_kwh: float
    petrol_litres: float
    diesel_litres: float
