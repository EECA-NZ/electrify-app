"""
Script to generate lookup table for the deviate PHP web app.
"""

import csv
import logging
import itertools
import os

from app.services.get_energy_plans import energy_plan
import app.services.configuration as cfg
from app.services.energy_calculator import emissions
from app.models.user_answers import (
    YourHomeAnswers,
    HeatingAnswers,
    HotWaterAnswers,
    CooktopAnswers,
    DrivingAnswers,
)

logging.basicConfig(level=logging.INFO)

# Constant for the lookup directory
LOOKUP_DIR = "../lookup/"

# Ensure the directory exists
os.makedirs(LOOKUP_DIR, exist_ok=True)

USER_PROVIDED = False
people_in_house = [1, 2, 3, 4, 5, 6]
postcodes = [f"{i:04d}" for i in range(1000, 3000)]  # Example: 2000 postcodes
disconnect_gas = [True, False]
main_heating_sources = [
    "Piped gas heater",
    "Bottled gas heater",
    "Heat pump",
    "Heat pump (ducted)",
    "Electric heater",
    "Wood burner",
]
heating_during_day = ["Never", "1-2 days a week", "3-4 days a week", "5-7 days a week"]
insulation_quality = ["Not well insulated", "Moderately insulated", "Well insulated"]
hot_water_usage = ["Low", "Average", "High"]
hot_water_heating_sources = [
    "Electric hot water cylinder",
    "Piped gas hot water cylinder",
    "Piped gas instantaneous",
    "Bottled gas instantaneous",
    "Hot water heat pump",
]
cooktop_types = [
    "Electric induction",
    "Piped gas",
    "Bottled gas",
    "Electric (coil or ceramic)",
]
vehicle_types = ["Petrol", "Diesel", "Hybrid", "Plug-in hybrid", "Electric"]
vehicle_sizes = ["Small", "Medium", "Large"]
km_per_week = ["50 or less", "100", "200", "300", "400 or more"]
has_solar = [True, False]  # Ignored for now


def calculate_cost_and_emissions(your_home, answers):
    """
    Use the answers and postcode to calculate cost and emissions.
    """
    energy_usage_profile = answers.energy_usage_pattern(your_home)
    my_plan = energy_plan(your_home.postcode)
    cost = my_plan.calculate_cost(energy_usage_profile)
    my_emissions = emissions(energy_usage_profile)
    return {"cost": cost, "emissions": my_emissions}


def generate_lookup_table_heating():
    """
    Produce lookup table for space heating.
    """
    combinations = itertools.product(
        people_in_house,
        postcodes,
        disconnect_gas,
        main_heating_sources,
        heating_during_day,
        insulation_quality,
    )
    my_csv = os.path.join(LOOKUP_DIR, "heating_lookup_table.csv")
    with open(my_csv, "w", newline="", encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "people_in_house",
                "postcode",
                "disconnect_gas",
                "main_heating_source",
                "heating_during_day",
                "insulation_quality",
                "annual_cost",
                "annual_co2e",
            ]
        )
        for combination in combinations:
            your_home = YourHomeAnswers(
                people_in_house=combination[0],
                postcode=combination[1],
                disconnect_gas=combination[2],
                user_provided=USER_PROVIDED,
            )
            heating = HeatingAnswers(
                main_heating_source=combination[3],
                heating_during_day=combination[4],
                insulation_quality=combination[5],
                user_provided=USER_PROVIDED,
            )
            cost_emissions = calculate_cost_and_emissions(your_home, heating)
            writer.writerow(
                list(combination)
                + [cost_emissions["cost"], cost_emissions["emissions"]]
            )


def generate_lookup_table_hot_water():
    """
    Produce lookup table for hot water heating.
    """
    combinations = itertools.product(
        people_in_house,
        postcodes,
        disconnect_gas,
        hot_water_usage,
        hot_water_heating_sources,
    )
    my_csv = os.path.join(LOOKUP_DIR, "hot_water_lookup_table.csv")
    with open(my_csv, "w", newline="", encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "people_in_house",
                "postcode",
                "disconnect_gas",
                "hot_water_usage",
                "hot_water_heating_source",
                "annual_cost",
                "annual_co2e",
            ]
        )
        for combination in combinations:
            your_home = YourHomeAnswers(
                people_in_house=combination[0],
                postcode=combination[1],
                disconnect_gas=combination[2],
                user_provided=USER_PROVIDED,
            )
            hot_water = HotWaterAnswers(
                hot_water_usage=combination[3],
                hot_water_heating_source=combination[4],
                user_provided=USER_PROVIDED,
            )
            cost_emissions = calculate_cost_and_emissions(your_home, hot_water)
            writer.writerow(
                list(combination)
                + [cost_emissions["cost"], cost_emissions["emissions"]]
            )


def generate_lookup_table_cooktop():
    """
    Produce lookup table for cooktops.
    """
    combinations = itertools.product(people_in_house, postcodes, disconnect_gas, cooktop_types)
    my_csv = os.path.join(LOOKUP_DIR, "cooktop_lookup_table.csv")
    with open(my_csv, "w", newline="", encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "people_in_house",
                "postcode",
                "disconnect_gas",
                "cooktop_type",
                "annual_cost",
                "annual_co2e"
            ]
        )
        for combination in combinations:
            your_home = YourHomeAnswers(
                people_in_house=combination[0],
                postcode=combination[1],
                disconnect_gas=combination[2],
                user_provided=USER_PROVIDED,
            )
            cooktop = CooktopAnswers(
                cooktop=combination[3],
                user_provided=USER_PROVIDED,
            )
            cost_emissions = calculate_cost_and_emissions(your_home, cooktop)
            writer.writerow(
                list(combination)
                + [cost_emissions["cost"], cost_emissions["emissions"]]
            )


def generate_lookup_table_vehicle():
    """
    Produce lookup table for vehicles.
    """
    combinations = itertools.product(
        people_in_house, postcodes, disconnect_gas, vehicle_types, vehicle_sizes, km_per_week
    )
    my_csv = os.path.join(LOOKUP_DIR, "vehicle_lookup_table.csv")
    with open(my_csv, "w", newline="", encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "people_in_house",
                "postcode",
                "disconnect_gas",
                "vehicle_type",
                "vehicle_size",
                "km_per_week",
                "annual_cost",
                "annual_co2e",
            ]
        )
        for combination in combinations:
            your_home = YourHomeAnswers(
                people_in_house=combination[0],
                postcode=combination[1],
                disconnect_gas=combination[2],
                user_provided=USER_PROVIDED,
            )
            driving = DrivingAnswers(
                vehicle_type=combination[3],
                vehicle_size=combination[4],
                km_per_week=combination[5],
                user_provided=USER_PROVIDED,
            )
            cost_emissions = calculate_cost_and_emissions(your_home, driving)
            writer.writerow(
                list(combination)
                + [cost_emissions["cost"], cost_emissions["emissions"]]
            )


def generate_all_lookup_tables():
    """
    Produce all lookup tables.
    """
    logging.info("Generating heating lookup table...")
    generate_lookup_table_heating()
    logging.info("Generating hot water lookup table...")
    generate_lookup_table_hot_water()
    logging.info("Generating cooktop lookup table...")
    generate_lookup_table_cooktop()
    logging.info("Generating vehicle lookup table...")
    generate_lookup_table_vehicle()


if __name__ == "__main__":
    generate_all_lookup_tables()
