from pydantic import BaseModel


class SpaceHeatingModel(BaseModel):
    area: float
    insulation_level: str
    average_temperature: float
    heating_type: str