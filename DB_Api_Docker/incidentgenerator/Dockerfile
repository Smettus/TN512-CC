FROM python:3.11

WORKDIR /app

COPY requirements_incident_generator.txt /app/

RUN pip install --no-cache-dir -r requirements_incident_generator.txt

COPY . /app/

WORKDIR /app

CMD ["python", "incident_generator.py"]