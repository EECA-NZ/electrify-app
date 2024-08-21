from fastapi import APIRouter, HTTPException
from ..models import WaterHeatingModel

router = APIRouter()

@router.post("/water-heating/")
def calculate_water_heating(data: WaterHeatingModel):
    try:
        result = perform_water_heating_calculation(data)
        return {"success": True, "energy_kwh": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def perform_water_heating_calculation(data: WaterHeatingModel):
    # Calculate the energy required for heating the water
    # Formula: energy (kWh) = volume (liters) * temp increase (C) * 0.001163 (kWh per liter per degree C)
    energy_required = data.volume_litres * data.temp_increase_celsius * 0.001163 / data.efficiency
    return energy_required
