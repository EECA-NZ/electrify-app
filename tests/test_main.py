"""
Currently all unit tests are housed here.

To run the tests, use the following command:

python -m pytest --verbose
"""

from pytest import approx

from fastapi.testclient import TestClient

from app.calculations import calculate_water_heating
from app.models.water_heating import WaterHeatingModel
from app.calculations import calculate_heating
from app.models.space_heating import SpaceHeatingModel
from app.models.energy_plans import HouseholdEnergyPlan
from app.services.configuration import get_default_electricity_plan
from app.services.configuration import get_default_natural_gas_plan
from app.services.configuration import get_default_lpg_plan
from app.services.configuration import get_default_usage_profile
from app.services.configuration import get_default_your_home_answers
from app.services.configuration import get_default_heating_answers
from app.services.configuration import get_default_hot_water_answers
from app.services.configuration import get_default_cooktop_answers
from app.services.configuration import get_default_driving_answers
from app.services.configuration import get_default_solar_answers
from app.models.answers import HouseholdEnergyProfileAnswers
from app.services.energy_usage_estimator import estimate_usage_from_profile
from app.constants import DAYS_IN_YEAR


from app.main import app


client = TestClient(app)


def test_read_root():
    """
    Test the root endpoint to ensure it returns the correct response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "<html>" in response.text


def test_startup_event(capsys):
    """
    Test the startup event to ensure the correct print output.
    """
    app.router.on_startup[0]()
    captured = capsys.readouterr()
    assert "Visit http://localhost:8000 or http://127.0.0.1:8000 to access the app." in captured.out


def test_calculate_heating():
    """
    Test the heating calculation logic.
    """
    test_input = SpaceHeatingModel(
        area=100,
        insulation_level="medium",
        average_temperature=22,
        heating_type="electric"
    )
    result = calculate_heating(test_input)
    assert result == {"cost": test_input.area * 5}


def test_calculate_water_heating():
    """
    Test the water heating calculation logic.
    """
    test_input = WaterHeatingModel(volume_litres=100, temp_increase_celsius=5, efficiency=0.8)
    result = calculate_water_heating(test_input)
    expected_energy = (test_input.volume_litres *
                       test_input.temp_increase_celsius *
                       0.001163 / test_input.efficiency)
    assert result["energy_required"] == expected_energy

def test_calculate_annual_costs():
    """
    Test the annual cost calculation logic.
    """
    my_plan = HouseholdEnergyPlan(
        name="Basic Household Energy Plan",
        electricity_plan=get_default_electricity_plan(),
        natural_gas_plan=get_default_natural_gas_plan(),
        lpg_plan=get_default_lpg_plan()
    )
    my_profile = get_default_usage_profile()
    my_cost = my_plan.calculate_cost(my_profile)
    expected_cost = 1111.25
    assert my_cost == expected_cost

def test_create_household_profile_answers():
    """
    Test the creation of a household profile answers object.
    """
    household_profile = HouseholdEnergyProfileAnswers(
        your_home=get_default_your_home_answers(),
        heating=get_default_heating_answers(),
        hot_water=get_default_hot_water_answers(),
        cooktop=get_default_cooktop_answers(),
        driving=get_default_driving_answers(),
        solar=get_default_solar_answers()
    )
    assert household_profile.your_home.people_in_house == 4
    assert household_profile.your_home.postcode == '0000'
    assert household_profile.driving.vehicle_type == 'Petrol'


def test_create_household_energy_profile_to_cost():
    """
    Test constructing a profile and plan, and doing a cost calculation.
    """
    household_profile = HouseholdEnergyProfileAnswers(
        your_home=get_default_your_home_answers(),
        heating=get_default_heating_answers(),
        hot_water=get_default_hot_water_answers(),
        cooktop=get_default_cooktop_answers(),
        driving=get_default_driving_answers(),
        solar=get_default_solar_answers()
    )
    my_plan = HouseholdEnergyPlan(
        name="Basic Household Energy Plan",
        electricity_plan=get_default_electricity_plan(),
        natural_gas_plan=get_default_natural_gas_plan(),
        lpg_plan=get_default_lpg_plan()
    )
    household_energy_use = estimate_usage_from_profile(household_profile)
    total_energy_costs = my_plan.calculate_cost(household_energy_use)
    assert total_energy_costs > 0


def test_cooking_energy_usage():
    """
    Test the energy usage pattern for cooking.
    """
    your_home = get_default_your_home_answers()
    cooktop = get_default_cooktop_answers()

    # Modeled energy use in kWh for each cooktop type. This is based
    # on a linearized energy use model that preserves the average
    # household energy use for cooking. (See 'Cooking' sheet of
    # supporting workbook.)
    expected_energy_use = {
        'Electric induction': [159, 239, 319, 398, 478, 558],
        'Piped gas': [412, 618, 824, 1030, 1236, 1442],
        'Bottled gas': [412, 618, 824, 1030, 1236, 1442, 1648],
        'Electric (coil or ceramic)': [176, 264, 352, 440, 528, 617]
    }

    # Expected field values based on cooktop type
    expected_values = {
        'Electric induction': {
            'elx_connection_days': DAYS_IN_YEAR,
            'night_kwh': 0,
            'controlled_kwh': 0,
            'natural_gas_kwh': 0,
            'lpg_kwh': 0,
            'natural_gas_connection_days': 0,
            'lpg_tank_rental_days': 0,
        },
        'Piped gas': {
            'elx_connection_days': 0,
            'day_kwh': 0,
            'night_kwh': 0,
            'controlled_kwh': 0,
            'lpg_kwh': 0,
            'natural_gas_connection_days': DAYS_IN_YEAR,
            'lpg_tank_rental_days': 0,
        },
        'Bottled gas': {
            'elx_connection_days': 0,
            'day_kwh': 0,
            'night_kwh': 0,
            'controlled_kwh': 0,
            'natural_gas_connection_days': 0,
            'lpg_tank_rental_days': 2 * DAYS_IN_YEAR,
        },
        'Electric (coil or ceramic)': {
            'elx_connection_days': DAYS_IN_YEAR,
            'night_kwh': 0,
            'controlled_kwh': 0,
            'natural_gas_kwh': 0,
            'lpg_kwh': 0,
            'natural_gas_connection_days': 0,
            'lpg_tank_rental_days': 0,
        },
    }

    for cooktop_type, energy_use_values in expected_energy_use.items():
        cooktop.cooktop = cooktop_type
        for i, expected_kwh in enumerate(energy_use_values):
            your_home.people_in_house = i + 1
            cooktop_energy_use = cooktop.energy_usage_pattern(your_home)

            # Assertions for expected energy usage (day_kwh, lpg_kwh, natural_gas_kwh)
            if cooktop_type in ['Electric induction', 'Electric (coil or ceramic)']:
                assert cooktop_energy_use.day_kwh == approx(expected_kwh, rel=1e-2)
            elif cooktop_type == 'Piped gas':
                assert cooktop_energy_use.natural_gas_kwh == approx(expected_kwh, rel=1e-2)
            elif cooktop_type == 'Bottled gas':
                assert cooktop_energy_use.lpg_kwh == approx(expected_kwh, rel=1e-2)

            # General assertions based on the cooktop type
            for field, expected_value in expected_values[cooktop_type].items():
                assert getattr(cooktop_energy_use, field) == expected_value,\
                    f"{field} failed for {cooktop_type}"
