"""
Deprecated
"""

from pydantic import BaseModel


class WaterHeatingModel(BaseModel):
    """
    Stub water heating model, to be retired.
    """
    volume_litres: float
    temp_increase_celsius: float
    efficiency: float
