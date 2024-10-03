from pydantic import BaseModel

class HouseholdYearlyFuelUsageProfile(BaseModel):
    elx_connection_days: float
    day_kwh: float
    night_kwh: float
    controlled_kwh: float
    natural_gas_connection_days: int
    natural_gas_kwh: float
    lpg_tank_rental_days: float
    lpg_kwh: float