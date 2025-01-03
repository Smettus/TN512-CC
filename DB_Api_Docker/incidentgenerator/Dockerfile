FROM python:3.11

WORKDIR /app

COPY requirements_incident_generator.txt /app/

RUN pip install --no-cache-dir -r requirements_incident_generator.txt

COPY . /app/

WORKDIR /app

# Download the 'wait-for-it' script
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it

CMD ["sh", "-c", "echo 'Waiting for django C2V2 api' && wait-for-it django:${DJANGO_PORT} -- python incident_generator.py"]
#CMD ["python", "incident_generator.py"]