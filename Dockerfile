# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

## Set the working directory in the container
#WORKDIR /usr/src/app
#
## Copy the current directory contents into the container at /usr/src/app
#COPY . .
#
## Install any needed packages specified in requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
#
## Make port 8000 available to the world outside this container
#EXPOSE 8000
#
## Define environment variable
#ENV NAME World
#
## Run app.py when the container launches
#CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container's workspace
COPY . /app

# Ensure pip is up to date
RUN pip install --upgrade pip 

# Install the package and its dependencies
RUN pip install -v --root-user-action=ignore .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Command to run the application
CMD ["electrify_app"]