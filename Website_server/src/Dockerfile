# Use the official Python image as the base image
FROM python:3.7

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . /app/

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements_frontend.txt

# Expose port 8000 for Django
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
