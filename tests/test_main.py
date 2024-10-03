from fastapi.testclient import TestClient

from app.calculations import calculate_water_heating
from app.models.water_heating import WaterHeatingModel
from app.calculations import calculate_heating
from app.models.space_heating import SpaceHeatingModel
from app.models.energy_plans import HouseholdEnergyPlan
from app.services.configuration import  get_default_electricity_plan, get_default_natural_gas_plan, get_default_lpg_plan, get_default_usage_profile
from app.services.configuration import get_default_your_home_answers, get_default_heating_answers, get_default_hot_water_answers, get_default_cooktop_answers, get_default_driving_answers, get_default_solar_answers
from app.models.answers import HouseholdEnergyProfileAnswers
from app.models.energy_plans import HouseholdEnergyPlan
from app.models.answers import HouseholdEnergyProfileAnswers
from app.services.energy_usage_estimator import estimate_usage_from_profile


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
    test_input = SpaceHeatingModel(area=100, insulation_level="medium", average_temperature=22, heating_type="electric")
    result = calculate_heating(test_input)
    assert result == {"cost": test_input.area * 5}


def test_calculate_water_heating():
    """
    Test the water heating calculation logic.
    """
    test_input = WaterHeatingModel(volume_litres=100, temp_increase_celsius=5, efficiency=0.8)
    result = calculate_water_heating(test_input)
    expected_energy = test_input.volume_litres * test_input.temp_increase_celsius * 0.001163 / test_input.efficiency
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
    assert household_profile.driving.vehicle == 'ICE'


def test_create_household_energy_profile_to_cost():
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