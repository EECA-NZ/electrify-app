from pydantic import BaseModel


class WaterHeatingModel(BaseModel):
    volume_litres: float
    temp_increase_celsius: float
    efficiency: float