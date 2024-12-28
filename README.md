# README - Running a Docker Compose File and Managing Containers

# Introduction
This guide explains how to use Docker Compose to manage Docker containers easily and quickly. It covers running `docker-compose.yml` files, the differences between the `-d` and `--build` options, and how to open one or more containers at the same time. Personally, I ran each container separately to ensure that each one works well.

# Attention: Database Data Loss
If you are using a container that contains a database (e.g., MySQL, PostgreSQL, etc.), the data in the database will be lost every time the container is removed. This is because data is stored in the container's filesystem, which is temporary by default.

To avoid data loss, you must configure persistent volumes in your docker-compose.yml file. These volumes allow you to persist the database data even if the container is removed or recreated. (not useful in our case)

Here is the `.yml` file to organise each container:

```yaml
networks:
  app_network:
    driver: bridge

services:
  
  db:
    image: mysql:5.7
    env_file:
      - .env 
    ports:
      - "${MYSQL_PORT}:${MYSQL_PORT}"  # Utilisation de la variable d'environnement
    networks:
      - app_network

  django:
    build:
      context: ./DB_Api_Docker/C2V2
    ports:
      - "${DJANGO_PORT}:${DJANGO_PORT}"
    depends_on:
      - db
    env_file:
      - .env  
    networks:
      - app_network

  planes_api:
    build:
      context: ./DB_Api_Docker/planes
    ports:
      - "${EXTERNAL_PORT_PLANE_API}:${INTERNAL_PORT_API}"
    depends_on:
      - db
      - django
    env_file:
      - .env  
    networks:
      - app_network

  ships_api:
    build:
      context: ./DB_Api_Docker/ships
    ports:
      - "${EXTERNAL_PORT_SHIP_API}:${INTERNAL_PORT_API}"
    depends_on:
      - db
      - django
    env_file:
      - .env 
    networks:
      - app_network

  frontend:
    build:
      context: ./Website_server/src
    depends_on:
      - db
      - django
    ports:
      - "${FRONTEND_PORT}:${FRONTEND_PORT}"
    env_file:
      - .env 
    volumes: 
      - ./Website_server/src/C_and_C/static:/app/C_and_C/static  # Monter C_and_C/static depuis le répertoire local
      - ./Website_server/src/accounts/static:/app/accounts/static  # Monter accounts/static depuis le répertoire local
    networks:
      - app_network
```
To make the dockerization more efficient, It can be useful to a `.env` file. The file below regroups all variable used in all containers. All `MYSQL_ statements` provides to create the MySQL container.
```env
  MYSQL_ROOT_PASSWORD=rootpassword
  MYSQL_DATABASE=mydb      # Doit correspondre à la variable attendue par MySQL
  MYSQL_USER=myuser
  MYSQL_PASSWORD=mypassword
  MYSQL_PORT=3306           # Port de la base de données MySQL
  MYSQL_HOST=db             # Nom du service Docker (db dans docker-compose.yml)
  DJANGO_URL=http://django:8080/api/tutorials
  DJANGO_PORT=8080
  EXTERNAL_PORT_PLANE_API=3000
  EXTERNAL_PORT_SHIP_API=4000
  INTERNAL_PORT_API=80
  FRONTEND_PORT=8000
```
# 1. Access the Directory Containing the `docker-compose.yml` File
Before running any Docker Compose commands, make sure you are in the directory containing the `docker-compose.yml` file. This file contains the configuration of the services that Docker Compose will manage (containers, networks, volumes, etc.).

Use the cd command to navigate to the directory where the docker-compose.yml file is located:
```bash
cd /path/to/your/folder
```
Replace `/path/to/your/folder` with the actual path to the directory containing the docker-compose.yml file.

# 2. Running a Docker Compose File
docker-compose up Command To start all the services defined in the docker-compose.yml file, use the following command:

`docker-compose up`
`docker-compose up -d --build`

* `-d`: Starts the containers in detached mode, without showing logs in the terminal. 
* `--build`: Forces the rebuild of the Docker images before starting the containers.

# 3. Running a Single Container
Docker Compose allows you to manage multiple services in a single `docker-compose.yml` file. If you want to run only a single service (container) from those defined in the file, you can specify the service as a parameter.

To run a specific container, use the following command, replacing `<service_name>` with the name of the service you want to start:
```bash
docker-compose up <service_name>
```
# 4. Managing Containers
Viewing Running Containers To display the list of running containers, use:

```bash
docker ps
```

This command is useful to display ID/Name of each container, which is useful for the next commands.

### Opening a Container
If you want to open a terminal inside a container to inspect or run commands, you can use the docker exec command. Here's an example for opening a terminal inside a MySQL container:

```bash
docker exec -it my_mysql bash
```

This command opens an interactive terminal (bash) inside the my_mysql container. Replace my_mysql with the name or ID of the container you want to inspect. For example, if you want to run the mysql container, you will be then able to check whether the database is first created and then fetched by django. Now you can go back to mysql and check if your tables are generated using the following codes:

```bash
docker exec -it my_mysql bash
```
Before performing commands in the `MY_SQL` container, you must authenticate using your root credentials, like this:

```bash
mysql -u root -p
```

* To see if all the tables are added: `show tables;`, you must get the following result:
  
![image](https://github.com/user-attachments/assets/659fe2fb-2435-4574-9831-3a4bc1d28e99)

* To see if the plane table is correctly configured: `describe plane;`, you should get this:
  
![image](https://github.com/user-attachments/assets/61fa5d99-4dde-4204-a2ef-9180b856cfd1)

### Stop a Specific Docker Container
To stop a running container, you can use the following command:
``` bash
docker stop <container_name_or_id>
```
Replace `<container_name_or_id>` with the name or ID of the container you want to stop.

### Stop All Containers and Images with Docker Compose
If you used Docker Compose to start your services, you can also stop and remove all the containers in your Compose project with:
``` bash
docker-compose down
```
This stops and removes the containers, networks, and volumes associated with the services (depending on the options used).

# 5. Run the project 
* Use the cd command to navigate to the directory where the docker-compose.yml file is located:
  
```bash
cd /path/to/your/folder
```
* Run the following containers:

```bash
docker-compose up db
```

```bash
docker-compose up django
```

```bash
docker-compose up planes_api
```

```bash
docker-compose up ships_api
```

```bash
docker-compose up frontend
```

or simply:

```bash
docker-compose up 
```

# Ensuring Django Waits for the Database to Be Ready
The last option is the most efficient one compared to previous methods. Indeed, by simply launching the docker-compose file, everything works correctly. However, even if you specify in your `docker-compose.yml` file that the Django container should wait for the database to be ready, Django may still attempt to connect to the database too early.

### Solution: Add `wait-for-it` to the Django Dockerfile
To solve this issue, you need to add the wait-for-it command in the Django container's Dockerfile. This will ensure that Django waits until the database is fully ready before trying to connect.

### Waiting for the Database to Be Ready Before Running Django
In the Dockerfile of the Django service, we have included a command that ensures the Django application only starts once the database is fully up and running. This is crucial because if Django starts before the database is ready, it will attempt to connect and fail, resulting in errors.

```bash
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it
```
This command downloads and installs the `wait-for-it` script, which is used to delay the start of Django until the database is accessible.

```bash
CMD ["sh", "-c", "echo 'Waiting for database to be ready...' && wait-for-it db:${MYSQL_PORT} -- python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:${DJANGO_PORT}"]
```
* ```wait-for-it db:${MYSQL_PORT}```: This waits for the database to be up and running on the specified port (using the value of MYSQL_PORT).
* ```python manage.py makemigrations```: After the database is ready, this command makes any necessary migrations for the Django application.
* ```python manage.py migrate```: Applies the migrations to ensure the database schema is up to date.
* ```python manage.py runserver 0.0.0.0:${DJANGO_PORT}```: Finally, it starts the Django application on the specified port (DJANGO_PORT).

### Why This is Necessary
Without this command, the Django application would attempt to connect to the database before it is ready, which would cause errors such as ```"Unable to connect to database."``` The ```wait-for-it``` script ensures that Django waits for the database service to be fully operational before attempting to connect, preventing these connection issues and ensuring smooth startup.


