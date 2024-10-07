"""
Main module to run the FastAPI application.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, responses
import uvicorn

# Import the app from component_savings_endpoints
from .api import household_energy_profile
from .api.component_savings_endpoints import app as component_savings_app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Lifespan event handler to run logic on startup and shutdown.
    """
    # Startup logic
    logger.info("Application %s is starting...", app_instance)
    print("Visit http://localhost:8000 or http://127.0.0.1:8000 to access the app.")
    yield  # This allows the application to run
    # Shutdown logic
    logger.info("Application is shutting down...")

# Pass the lifespan handler when creating the FastAPI instance
app = FastAPI(lifespan=lifespan)

@app.get("/")
def main():
    """
    Function to redirect to the documentation.
    """
    return responses.RedirectResponse(url='/docs/')

# Include the router for the household energy profile
app.include_router(household_energy_profile.router)

# Include the router for component savings endpoints
app.include_router(component_savings_app.router)

def run():
    """
    Function to run the Uvicorn server.
    """
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
