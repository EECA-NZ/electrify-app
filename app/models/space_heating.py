"""
Deprecated
"""

from pydantic import BaseModel


class SpaceHeatingModel(BaseModel):
    """
    Stub space heating model, to be retired.
    """
    area: float
    insulation_level: str
    average_temperature: float
    heating_type: str
