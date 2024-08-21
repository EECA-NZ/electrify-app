from fastapi import APIRouter, Body
from ..models import SpaceHeatingModel
from ..calculations import calculate_heating

router = APIRouter()

@router.post("/space-heating/")
def space_heating(data: SpaceHeatingModel):
    result = calculate_heating(data)
    return {"success": True, "data": result}
