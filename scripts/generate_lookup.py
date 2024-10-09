"""
Script to generate lookup table for the deviate PHP web app.
"""

import os
import logging
import itertools
import pandas as pd

from app.services.get_energy_plans import energy_plan
from app.services.get_climate_zone import climate_zone
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
LOOKUP_DIR = "../lookup"

REPORT_EVERY_N_ROWS = 1E5

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

# Cache for expensive functions
energy_plan_cache = {}
climate_zone_cache = {}
cost_emissions_cache = {}


def clear_output_dir(output_dir):
    """
    Clear the output directory.
    """
    for file in os.listdir(output_dir):
        if file.endswith(".csv"):
            os.remove(os.path.join(output_dir, file))

def uniquify_rows_and_write_to_csv(raw_df, filename):
    """
    Write unique rows to a CSV file.
    """
    final_df = raw_df.drop_duplicates().reset_index(drop=True)
    final_df.to_csv(filename, index=False)
    return final_df

def get_energy_plan_cached(postcode):
    """
    Cached version of energy_plan function.
    """
    if postcode in energy_plan_cache:
        return energy_plan_cache[postcode]
    plan = energy_plan(postcode)
    energy_plan_cache[postcode] = plan
    return plan

def get_climate_zone_cached(postcode):
    """
    Cached version of climate_zone function.
    """
    if postcode in climate_zone_cache:
        return climate_zone_cache[postcode]
    zone = climate_zone(postcode)
    climate_zone_cache[postcode] = zone
    return zone

def calculate_cost_and_emissions(your_home, answers):
    """
    Use the answers and postcode to calculate cost and emissions.
    """
    # Create a cache key based on the attributes of your_home and answers
    cache_key = (
        your_home.people_in_house,
        your_home.postcode,
        your_home.disconnect_gas,
        tuple(sorted(answers.__dict__.items())),
    )

    if cache_key in cost_emissions_cache:
        return cost_emissions_cache[cache_key]

    energy_usage_profile = answers.energy_usage_pattern(your_home)
    my_plan = get_energy_plan_cached(your_home.postcode)
    cost = my_plan.calculate_cost(energy_usage_profile)
    my_emissions = emissions(energy_usage_profile)
    result = {"cost": cost, "emissions": my_emissions}
    cost_emissions_cache[cache_key] = result
    return result

def generate_postcode_lookup_table():
    """
    Generate the postcode lookup table.
    """
    rows = []
    for postcode in postcodes:
        my_plan = get_energy_plan_cached(postcode)
        my_climate_zone = get_climate_zone_cached(postcode)
        row = {
            "postcode": postcode,
            "climate_zone": my_climate_zone,
            "electricity_plan_name": my_plan.electricity_plan.name,
            "natural_gas_plan_name": my_plan.natural_gas_plan.name,
            "lpg_plan_name": my_plan.lpg_plan.name,
            "wood_price_name": my_plan.wood_price.name,
            "petrol_price_name": my_plan.petrol_price.name,
            "diesel_price_name": my_plan.diesel_price.name,
        }
        rows.append(row)
    postcode_df = pd.DataFrame(rows)
    return uniquify_rows_and_write_to_csv(
        postcode_df,
        os.path.join(LOOKUP_DIR, "postcode_to_climate_and_energy_plans.csv"),
    )

def generate_heating_lookup_table():
    """
    Generate the heating lookup table.
    """
    heating_rows = []
    for combination in itertools.product(
        people_in_house,
        postcodes,
        disconnect_gas,
        main_heating_sources,
        heating_during_day,
        insulation_quality,
    ):
        people, postcode, disconnect, heating_source, heating_day, insulation = combination

        your_home = YourHomeAnswers(
            people_in_house=people,
            postcode=postcode,
            disconnect_gas=disconnect,
            user_provided=USER_PROVIDED,
        )
        heating = HeatingAnswers(
            main_heating_source=heating_source,
            heating_during_day=heating_day,
            insulation_quality=insulation,
            user_provided=USER_PROVIDED,
        )
        cost_emissions = calculate_cost_and_emissions(your_home, heating)
        my_plan = get_energy_plan_cached(postcode)
        my_climate_zone = get_climate_zone_cached(postcode)

        row = {
            "climate_zone": my_climate_zone,
            "electricity_plan_name": my_plan.electricity_plan.name,
            "natural_gas_plan_name": my_plan.natural_gas_plan.name,
            "lpg_plan_name": my_plan.lpg_plan.name,
            "wood_price_name": my_plan.wood_price.name,
            "petrol_price_name": my_plan.petrol_price.name,
            "diesel_price_name": my_plan.diesel_price.name,
            "people_in_house": people,
            "disconnect_gas": disconnect,
            "main_heating_source": heating_source,
            "heating_during_day": heating_day,
            "insulation_quality": insulation,
            "annual_variable_cost": cost_emissions["cost"],
            "annual_co2e": cost_emissions["emissions"],
        }
        heating_rows.append(row)

        if len(heating_rows) % REPORT_EVERY_N_ROWS == 0:
            logging.info("Appended %s rows to heating_rows.", len(heating_rows))

    space_heating_df = pd.DataFrame(heating_rows)
    return uniquify_rows_and_write_to_csv(
        space_heating_df, os.path.join(LOOKUP_DIR, "space_heating_lookup_table.csv")
    )

def generate_hot_water_lookup_table():
    """
    Generate the hot water lookup table.
    """
    hot_water_rows = []
    for combination in itertools.product(
        people_in_house,
        postcodes,
        disconnect_gas,
        hot_water_usage,
        hot_water_heating_sources,
    ):
        people, postcode, disconnect, usage, heating_source = combination

        your_home = YourHomeAnswers(
            people_in_house=people,
            postcode=postcode,
            disconnect_gas=disconnect,
            user_provided=USER_PROVIDED,
        )
        hot_water = HotWaterAnswers(
            hot_water_usage=usage,
            hot_water_heating_source=heating_source,
            user_provided=USER_PROVIDED,
        )
        cost_emissions = calculate_cost_and_emissions(your_home, hot_water)
        my_plan = get_energy_plan_cached(postcode)
        my_climate_zone = get_climate_zone_cached(postcode)

        row = {
            "climate_zone": my_climate_zone,
            "electricity_plan_name": my_plan.electricity_plan.name,
            "natural_gas_plan_name": my_plan.natural_gas_plan.name,
            "lpg_plan_name": my_plan.lpg_plan.name,
            "wood_price_name": my_plan.wood_price.name,
            "petrol_price_name": my_plan.petrol_price.name,
            "diesel_price_name": my_plan.diesel_price.name,
            "people_in_house": people,
            "disconnect_gas": disconnect,
            "hot_water_usage": usage,
            "hot_water_heating_source": heating_source,
            "annual_variable_cost": cost_emissions["cost"],
            "annual_co2e": cost_emissions["emissions"],
        }
        hot_water_rows.append(row)

        if len(hot_water_rows) % REPORT_EVERY_N_ROWS == 0:
            logging.info("Appended %s rows to hot_water_rows.", len(hot_water_rows))

    hot_water_df = pd.DataFrame(hot_water_rows)
    return uniquify_rows_and_write_to_csv(
        hot_water_df, os.path.join(LOOKUP_DIR, "hot_water_lookup_table.csv")
    )

def generate_cooktop_lookup_table():
    """
    Generate the cooktop lookup table.
    """
    cooktop_rows = []
    for combination in itertools.product(
        people_in_house, postcodes, disconnect_gas, cooktop_types
    ):
        people, postcode, disconnect, cooktop_type = combination

        your_home = YourHomeAnswers(
            people_in_house=people,
            postcode=postcode,
            disconnect_gas=disconnect,
            user_provided=USER_PROVIDED,
        )
        cooktop = CooktopAnswers(
            cooktop=cooktop_type,
            user_provided=USER_PROVIDED,
        )
        cost_emissions = calculate_cost_and_emissions(your_home, cooktop)
        my_plan = get_energy_plan_cached(postcode)
        my_climate_zone = get_climate_zone_cached(postcode)

        row = {
            "climate_zone": my_climate_zone,
            "electricity_plan_name": my_plan.electricity_plan.name,
            "natural_gas_plan_name": my_plan.natural_gas_plan.name,
            "lpg_plan_name": my_plan.lpg_plan.name,
            "wood_price_name": my_plan.wood_price.name,
            "petrol_price_name": my_plan.petrol_price.name,
            "diesel_price_name": my_plan.diesel_price.name,
            "people_in_house": people,
            "disconnect_gas": disconnect,
            "cooktop_type": cooktop_type,
            "annual_variable_cost": cost_emissions["cost"],
            "annual_co2e": cost_emissions["emissions"],
        }
        cooktop_rows.append(row)

        if len(cooktop_rows) % REPORT_EVERY_N_ROWS == 0:
            logging.info("Appended %s rows to cooktop_rows.", len(cooktop_rows))

    cooktop_df = pd.DataFrame(cooktop_rows)
    return uniquify_rows_and_write_to_csv(
        cooktop_df, os.path.join(LOOKUP_DIR, "cooktop_lookup_table.csv")
    )

def generate_vehicle_lookup_table():
    """
    Generate the vehicle lookup table.
    """
    vehicle_rows = []
    for combination in itertools.product(
        people_in_house,
        postcodes,
        disconnect_gas,
        vehicle_types,
        vehicle_sizes,
        km_per_week,
    ):
        people, postcode, disconnect, vehicle_type, vehicle_size, kilometers = combination

        your_home = YourHomeAnswers(
            people_in_house=people,
            postcode=postcode,
            disconnect_gas=disconnect,
            user_provided=USER_PROVIDED,
        )
        driving = DrivingAnswers(
            vehicle_type=vehicle_type,
            vehicle_size=vehicle_size,
            km_per_week=kilometers,
            user_provided=USER_PROVIDED,
        )
        cost_emissions = calculate_cost_and_emissions(your_home, driving)
        my_plan = get_energy_plan_cached(postcode)
        my_climate_zone = get_climate_zone_cached(postcode)

        row = {
            "climate_zone": my_climate_zone,
            "electricity_plan_name": my_plan.electricity_plan.name,
            "natural_gas_plan_name": my_plan.natural_gas_plan.name,
            "lpg_plan_name": my_plan.lpg_plan.name,
            "wood_price_name": my_plan.wood_price.name,
            "petrol_price_name": my_plan.petrol_price.name,
            "diesel_price_name": my_plan.diesel_price.name,
            "people_in_house": people,
            "disconnect_gas": disconnect,
            "vehicle_type": vehicle_type,
            "vehicle_size": vehicle_size,
            "km_per_week": kilometers,
            "annual_variable_cost": cost_emissions["cost"],
            "annual_co2e": cost_emissions["emissions"],
        }
        vehicle_rows.append(row)

        if len(vehicle_rows) % REPORT_EVERY_N_ROWS == 0:
            logging.info("Appended %s rows to vehicle_rows.", len(vehicle_rows))

    vehicle_df = pd.DataFrame(vehicle_rows)
    return uniquify_rows_and_write_to_csv(
        vehicle_df, os.path.join(LOOKUP_DIR, "vehicle_lookup_table.csv")
    )

def generate_natural_gas_fixed_cost_lookup_table():
    """
    Generate the natural gas fixed cost lookup table.
    """
    natural_gas_fixed_cost_rows = []
    for postcode in postcodes:
        my_plan = get_energy_plan_cached(postcode)
        row = {
            "natural_gas_plan_name": my_plan.natural_gas_plan.name,
            "natural_gas_daily_charge": my_plan.natural_gas_plan.daily_charge,
        }
        natural_gas_fixed_cost_rows.append(row)
    natural_gas_fixed_costs_df = pd.DataFrame(natural_gas_fixed_cost_rows)
    return uniquify_rows_and_write_to_csv(
        natural_gas_fixed_costs_df,
        os.path.join(LOOKUP_DIR, "natural_gas_fixed_cost_lookup_table.csv"),
    )

def generate_lpg_fixed_cost_lookup_table():
    """
    Generate the LPG fixed cost lookup table.
    """
    lpg_fixed_cost_rows = []
    for postcode in postcodes:
        my_plan = get_energy_plan_cached(postcode)
        row = {
            "lpg_plan_name": my_plan.lpg_plan.name,
            "lpg_daily_charge": my_plan.lpg_plan.daily_charge,
        }
        lpg_fixed_cost_rows.append(row)
    lpg_fixed_costs_df = pd.DataFrame(lpg_fixed_cost_rows)
    return uniquify_rows_and_write_to_csv(
        lpg_fixed_costs_df,
        os.path.join(LOOKUP_DIR, "lpg_fixed_cost_lookup_table.csv"),
    )


#### MAIN ####

clear_output_dir(LOOKUP_DIR)
logging.info("Generating postcode lookup table...")
postcode_table = generate_postcode_lookup_table()
logging.info("Generating heating lookup table...")
heating_table = generate_heating_lookup_table()
logging.info("Generating hot water lookup table...")
hotwater_table = generate_hot_water_lookup_table()
logging.info("Generating cooktop lookup table...")
cooktop_table = generate_cooktop_lookup_table()
logging.info("Generating vehicle lookup table...")
vehicle_table = generate_vehicle_lookup_table()
logging.info("Generating natural gas fixed cost lookup table...")
natural_gas_fixed_cost_table = generate_natural_gas_fixed_cost_lookup_table()
logging.info("Generating LPG fixed cost lookup table...")
lpg_fixed_cost_table = generate_lpg_fixed_cost_lookup_table()
