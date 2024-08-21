# Electrify App

## Introduction
This repository contains the source code for the Electrify App, a FastAPI application designed to provide insights into household energy costs. It's designed to be easy to deploy both locally and as a Docker container.

## Prerequisites
Before running the application, ensure you have Python and Docker installed on your system. Python 3.12 or higher is recommended.

## Local Setup
1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
    ```

1. **Upgrade pip and install dependencies:**
    ```bash
    python -m pip install --upgrade pip
    python -m pip install .
    ```

1. **Run the test suite:**
    ```bash
    python -m pytest
    ```

1. **Run the application locally:**
    ```bash
    Use Uvicorn to run the application with live reloading:
    python -m uvicorn app.main:app --reload # The --reload option makes the server restart after code changes.
    ```

1. **Access the application:**
    Point your browser at `http://localhost:8000` or `http://localhost:8000/docs` to see the Swagger UI.

1. **Post a request to the API:**
    ```bash
    curl -Method 'POST' `
     -Uri 'http://localhost:8000/water-heating/' `
     -Headers @{ "Accept"="application/json"; "Content-Type"="application/json" } `
     -Body '{
        "volume_litres": 100,
        "temp_increase_celsius": 50,
        "efficiency": 0.8
     }'
    ```

## Docker Setup

1. **Build the Docker image:**
    ```bash
    docker build -t electrify-app .
    ```

1. **Run the Docker container:**
    ```bash
    docker run --rm -p 8000:8000 electrify-app
    ```

## Accessing the application

* **Local web URL:** Point your browser at `http://localhost:8000` to view the application.

* **Swagger UI:** Access the Swagger UI by navigating to `http://localhost:8000/docs` where you can see and interact with the API's resources.

## Additional notes

* The Docker setup runs the application on port 8000, make sure this port is available on your machine.
* The API uses FastAPI, which provides automatic interactive API documentation (Swagger UI), making it easier to visualize and interact with the API's endpoints.