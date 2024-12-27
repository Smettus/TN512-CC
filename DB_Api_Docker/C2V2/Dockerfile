# Base image
FROM python:3.7

# Set the working directory
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements_DB.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements_DB.txt

# Copy the rest of the project
COPY . /app/

# Expose the port
EXPOSE 8080

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]