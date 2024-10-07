from fastapi import FastAPI
import logging
from ..models.answers import HeatingAnswers, HotWaterAnswers, CooktopAnswers, DrivingAnswers, SolarAnswers, YourHomeAnswers
from ..services.cost_calculator import calculate_savings_options

# Set up logging
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/heating/savings")
async def heating_savings(heating_answers: HeatingAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for heating options.
    """
    try:
        logger.info(f"Received heating answers: {heating_answers}")
        options = calculate_savings_options(heating_answers, 'main_heating_source', your_home)
        logger.info(f"Found heating options: {options}")
        return {"options": options}
    except Exception as e:
        logger.error(f"Error calculating heating savings: {e}")
        return {"error": "Error calculating heating savings"}


@app.post("/hot_water/savings")
async def hot_water_savings(hot_water_answers: HotWaterAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for hot water heating options.
    """
    try:
        logger.info(f"Received hot water answers: {hot_water_answers}")
        options = calculate_savings_options(hot_water_answers, 'hot_water_heating_source', your_home)
        logger.info(f"Found hot water options: {options}")
        return {"options": options}
    except Exception as e:
        logger.error(f"Error calculating hot water savings: {e}")
        return {"error": "Error calculating hot water savings"}


@app.post("/cooktop/savings")
async def cooktop_savings(cooktop_answers: CooktopAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for cooking options.
    """
    try:
        logger.info(f"Received cooktop answers: {cooktop_answers}")
        options = calculate_savings_options(cooktop_answers, 'cooktop', your_home)
        logger.info(f"Found cooktop options: {options}")
        return {"options": options}
    except Exception as e:
        logger.error(f"Error calculating cooktop savings: {e}")
        return {"error": "Error calculating cooktop savings"}


@app.post("/driving/savings")
async def driving_savings(driving_answers: DrivingAnswers, your_home: YourHomeAnswers):
    """
    Endpoint to calculate savings for driving options.
    """
    try:
        logger.info(f"Received driving answers: {driving_answers}")
        options = calculate_savings_options(driving_answers, 'vehicle_type', your_home)
        logger.info(f"Found driving options: {options}")
        return {"options": options}
    except Exception as e:
        logger.error(f"Error calculating driving savings: {e}")
        return {"error": "Error calculating driving savings"}
