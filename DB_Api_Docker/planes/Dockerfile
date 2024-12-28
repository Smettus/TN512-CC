# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the entire project folder (including the Python scripts and the opensky-api folder)
COPY . /app/

# Navigate to the directory containing the package (opensky-api/python)
WORKDIR /app/opensky-api/python

# Install the OpenSky API package in editable mode
RUN pip install -e .

# Return to the root app directory
WORKDIR /app

# Install other dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements_FLIGHTAPI.txt

CMD ["python", "flight_api.py"]


