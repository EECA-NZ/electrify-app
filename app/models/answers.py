from typing import Literal, Optional
from pydantic import BaseModel, constr, conint, confloat

class YourHomeAnswers(BaseModel):
    people_in_house: conint(ge=1)
    postcode: constr(strip_whitespace=True,
                     pattern=r'^\d{4}$')

class HeatingAnswers(BaseModel):
    main_heating_source: Literal[
        'Electric heater',
        'Wood burner',
        'Heat pump',
        'Bottled gas heater',
        'Gas central heating',
        'Gas heater',
        'Coal range',
        'Heat Pump (ducted)'
    ]
    heating_during_day: Literal['Yes', 'No']
    insulation_quality: Literal[
        'Not well insulated',
        'Somewhere in between',
        'Well insulated']

class HotWaterAnswers(BaseModel):
    hot_water_usage: Literal['Low', 'Medium', 'High']
    hot_water_heating_source: Literal[
        'Gas hot water cylinder',
        'Gas continuous hot water',
        'Electric hot water cylinder',
        'Electric continuous hot water',
        'Hot water heat pump',
        'Wetback',
        'Solar hot water',
        'No hot water',
        'Unsure'
    ]

class CooktopAnswers(BaseModel):
    cooktop: Literal[
        'Electric induction',
        'Gas hob',
        'Electric']

class DrivingAnswers(BaseModel):
    vehicle: Literal[
        'EV',
        'ICE'
    ]
    usage: Literal[
        'Low',
        'Medium',
        'High'
    ]

class SolarAnswers(BaseModel):
    arraySizekW: confloat(ge=0)
    inverterSizekW: confloat(ge=0)

class HouseholdEnergyProfile(BaseModel):
    your_home: Optional[YourHomeAnswers] = None
    heating: Optional[HeatingAnswers] = None
    hot_water: Optional[HotWaterAnswers] = None
    cooktop: Optional[CooktopAnswers] = None
    driving: Optional[DrivingAnswers] = None
    solar: Optional[SolarAnswers] = None