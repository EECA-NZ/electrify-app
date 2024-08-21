from pydantic import BaseModel


class SpaceHeatingModel(BaseModel):
    area: float
    insulation_level: str
    average_temperature: float
    heating_type: str


class WaterHeatingModel(BaseModel):
    volume_litres: float
    temp_increase_celsius: float
    efficiency: float