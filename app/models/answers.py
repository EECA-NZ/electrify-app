from pydantic import BaseModel

class EnergyUsageAnswers(BaseModel):
    heating: str
    cooling: str
    appliances: str
    lighting: str
    electronics: str

class InsulationAnswers(BaseModel):
    walls: str
    attic: str
    windows: str
