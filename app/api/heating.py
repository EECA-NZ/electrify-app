"""
API for calculating the energy required for heating water. Deprecated.
"""

from fastapi import APIRouter
from ..models.space_heating import SpaceHeatingModel
from ..calculations import calculate_heating

router = APIRouter()


@router.post("/space-heating/")
def space_heating(data: SpaceHeatingModel):
    """
    Calculate the energy required for
    heating a space. Stub. Deprecated.
    """
    result = calculate_heating(data)
    return {"success": True, "data": result}
