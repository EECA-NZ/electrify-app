"""
Main module to run the FastAPI application.
"""

from fastapi import FastAPI, responses
import uvicorn

from .api import household_energy_profile

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """Function to run on startup."""
    print("Visit http://localhost:8000 or http://127.0.0.1:8000 to access the app.")

@app.get("/")
def main():
    """Function to redirect to the documentation."""
    return responses.RedirectResponse(url='/docs/')

app.include_router(household_energy_profile.router)

def run():
    """Function to run the Uvicorn server."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
