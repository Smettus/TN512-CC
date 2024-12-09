import os
import shutil
import subprocess
import mysql.connector # pip install mysql-connector-python

db_config = {
    "host": "localhost",
    "user": "smettus",  # Replace with your MySQL username
    "password": "derp",  # Replace with your MySQL password
}
dbpath = "./DB_Api/C2V2/"
db_sql_file = "./DB_Api/C2V2/C2V2/db.sql"
migrations_dir = "./DB_Api/C2V2/tutorials/migrations"

def clean_migrations(directory):
    """
    Deletes all migration files except __init__.py and pycache folders.
    """
    print(f"Cleaning migrations in {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file != "__init__.py" and not file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))
    print("Migration cleanup complete.")

def execute_sql_file(cursor, file_path):
    """
    Executes all SQL commands from the provided SQL file.
    """
    print(f"Executing SQL file: {file_path}")
    with open(file_path, "r") as sql_file:
        sql_commands = sql_file.read()
        for command in sql_commands.split(';'):
            if command.strip():
                try:
                    cursor.execute(command)
                except mysql.connector.Error as err:
                    print(f"Error executing command: {command}\n{err}")
    print("SQL file executed successfully.")
    
def reset_database():
    """
    Drops the database, recreates it, and reloads the schema from the SQL file.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        print("Dropping and recreating database 'C2'...")
        cursor.execute("DROP DATABASE IF EXISTS C2;")
        cursor.execute("CREATE DATABASE C2;")
        print("Database 'C2' reset successfully.")
        
        cursor.execute("USE C2;")

        if os.path.exists(db_sql_file):
            execute_sql_file(cursor, db_sql_file)
        else:
            print(f"Error: SQL file not found at {db_sql_file}")

        connection.commit()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")
            
def run_django_migrations(path):
    """
    Runs Django management commands (makemigrations and migrate).
    """
    print("Running Django management commands...")
    try:
        subprocess.run(["python", "manage.py", "makemigrations"], cwd=path, check=True)
        subprocess.run(["python", "manage.py", "migrate"], cwd=path, check=True)
        print("Django migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Django commands: {e}")

if __name__ == "__main__":
    # Step 1: Clean migrations
    clean_migrations(migrations_dir)

    # Step 2: Reset the database
    reset_database()
    
    # Step 3: Migrate the database
    run_django_migrations(dbpath)

    print("Database reset and migration cleanup complete!")
