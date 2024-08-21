from .models import SpaceHeatingModel, WaterHeatingModel

def calculate_heating(data: SpaceHeatingModel):
    # Implement calculation logic here
    return {"cost": data.area * 5}  # Dummy example

def calculate_water_heating(data: WaterHeatingModel):
    # Calculate the energy required for heating the water
    # Formula: energy (kWh) = volume (litres) * temp increase (C) * 0.001163 (kWh per litre per degree C)
    energy_required = data.volume_litres * data.temp_increase_celsius * 0.001163 / data.efficiency
    return {"energy_required": energy_required}
