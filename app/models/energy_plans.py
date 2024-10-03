from pydantic import BaseModel

class ElectricityPlan(BaseModel):
    name: str
    nzd_per_day_kwh: float
    nzd_per_night_kwh: float
    nzd_per_controlled_kwh: float
    daily_charge: float

    def calculate_cost(self, profile):
        return (profile.day_kwh * self.nzd_per_day_kwh +
                profile.night_kwh * self.nzd_per_night_kwh +
                profile.controlled_kwh * self.nzd_per_controlled_kwh +
                profile.elx_connection_days * self.daily_charge)

class NaturalGasPlan(BaseModel):
    name: str
    per_natural_gas_kwh: float
    daily_charge: float

    def calculate_cost(self, profile):
        return (profile.natural_gas_kwh * self.per_natural_gas_kwh +
                profile.natural_gas_connection_days * self.daily_charge)

class LPGPlan(BaseModel):
    name: str
    per_lpg_kwh: float
    daily_charge: float

    def calculate_cost(self, profile):
        return (profile.lpg_kwh * self.per_lpg_kwh +
                profile.lpg_tank_rental_days * self.daily_charge)

class HouseholdEnergyPlan(BaseModel):
    name: str
    electricity_plan: ElectricityPlan
    natural_gas_plan: NaturalGasPlan
    lpg_plan: LPGPlan

    def calculate_cost(self, profile):
        return (self.electricity_plan.calculate_cost(profile) +
                self.natural_gas_plan.calculate_cost(profile) +
                self.lpg_plan.calculate_cost(profile))