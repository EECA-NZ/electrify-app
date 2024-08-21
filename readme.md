# Electrify App

This repository contains the source code for the Electrify App, a FastAPI application designed to provide insights into household energy costs. It's designed to be easy to deploy as a Docker container and also easy to use locally as a library.

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

1. **Run a script using the library:**
    ```bash
    cd scripts
    python run_heating_analysis.py
    ```

1. **Run the application locally:**
    Use Uvicorn to run the application with live reloading to restart the server after code changes:
    ```bash
    python -m uvicorn app.main:app --reload
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


## Deploying the EV Roam Container

This section provides step-by-step instructions for building, pushing, and deploying the `electrify-app` Docker container to Azure.

### Azure Login

Login to Azure:

```
az login --scope https://management.core.windows.net//.default
```

### Set Environment Variables

Define necessary environment variables:

```powershell
$resourceGroup = "eeca-rg-DWBI-dev-aue"
$acrName = "eecaacrdwbidevaue"
$location = "australiaeast"
$containerGroupName = "aci-evroam"
$acrPassword = az acr credential show -n $acrName --query "passwords[0].value" -o tsv
$loginServer = az acr show -n $acrName --query loginServer --output tsv
$image = "electrify-app:0.1.0"
$imageTag = "$loginServer/$image"
```

### Docker Operations

Login to Docker, build the Docker image, tag it, and push it to Azure Container Registry:

```
docker login -u $acrName -p $acrPassword $loginServer
docker build -t $image .
docker tag $image $imageTag
docker push $imageTag
```

### Azure Container Instance Deployment

Create the Azure Container Instance:

```powershell
az container create -g $resourceGroup -n $containerGroupName --registry-username $acrName --registry-password $acrPassword --image $imageTag --cpu 1 --memory 1 --dns-name-label "aciacr" --ports 8000 --restart-policy Always
```

Verify the container and view its logs:

```
az container show -g $resourceGroup -n $containerGroupName
az container logs -g $resourceGroup -n $containerGroupName
```

### Accessing the Application

Point your browser at:

```
http://aciacr.australiaeast.azurecontainer.io:8000/
```

### Cleanup

Delete the container when done:

```
az container delete -g $resourceGroup -n $containerGroupName
```