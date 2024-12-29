# Base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements_DB.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements_DB.txt

# Copy the rest of the project
COPY . /app/

# Download the 'wait-for-it' script
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it

# Command to wait for DB to be ready before running Django # docker run -it <container name>, for debbuging.
#CMD ["bash"]
# Need the internal port which is 3306 though
CMD ["sh", "-c", "echo 'Waiting for database to be ready...' && wait-for-it db:${MYSQL_INTERNAL_PORT} -- python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:${DJANGO_PORT}"]
#CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:${DJANGO_PORT}"]