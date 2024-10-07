"""
This module provides functions to estimate savings for individual
components of the home.
"""

import logging
from fastapi import FastAPI
from ..models.user_answers import (
    HeatingAnswers,
    HotWaterAnswers,
    CooktopAnswers,
    DrivingAnswers,
    YourHomeAnswers,
)
from ..services.cost_calculator import calculate_savings_options

# Set up logging
logger = logging.getLogger(__name__)

app = FastAPI()


# pylint: disable=broad-exception-caught
@app.post("/heating/savings")
async def heating_savings(heating_answers: HeatingAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for heating options.
    """
    try:
        logger.info("Received heating answers: %s", heating_answers)
        options = calculate_savings_options(
            heating_answers, "main_heating_source", your_home
        )
        logger.info("Found heating options: %s", options)
        return {"options": options}
    except Exception as e:
        logger.error("Error calculating heating savings: %s", e)
        return {"error": "Error calculating heating savings"}


@app.post("/hot_water/savings")
async def hot_water_savings(
    hot_water_answers: HotWaterAnswers, your_home: YourHomeAnswers
):
    """
    Endpoint to calculate savings for hot water heating options.
    """
    try:
        logger.info("Received hot water answers: %s", hot_water_answers)
        options = calculate_savings_options(
            hot_water_answers, "hot_water_heating_source", your_home
        )
        logger.info("Found hot water options: %s", options)
        return {"options": options}
    except Exception as e:
        logger.error("Error calculating hot water savings: %s", e)
        return {"error": "Error calculating hot water savings"}


@app.post("/cooktop/savings")
async def cooktop_savings(cooktop_answers: CooktopAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for cooking options.
    """
    try:
        logger.info("Received cooktop answers: %s", cooktop_answers)
        options = calculate_savings_options(cooktop_answers, "cooktop", your_home)
        logger.info("Found cooktop options: %s", options)
        return {"options": options}
    except Exception as e:
        logger.error("Error calculating cooktop savings: %s", e)
        return {"error": "Error calculating cooktop savings"}


@app.post("/driving/savings")
async def driving_savings(driving_answers: DrivingAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for driving options.
    """
    try:
        logger.info("Received driving answers: %s", driving_answers)
        options = calculate_savings_options(driving_answers, "vehicle_type", your_home)
        logger.info("Found driving options: %s", options)
        return {"options": options}
    except Exception as e:
        logger.error("Error calculating driving savings: %s", e)
        return {"error": "Error calculating driving savings"}
