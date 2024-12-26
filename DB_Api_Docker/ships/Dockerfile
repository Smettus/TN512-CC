FROM python:3.7

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the entire project folder (including the Python scripts and the opensky-api folder)
COPY . /app/

# Install other dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements_Ships.txt

# Set the default command to run your Python script
CMD ["python", "ship_api.py"]