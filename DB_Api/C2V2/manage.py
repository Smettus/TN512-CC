#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.db import connection
import pymysql


def main():
    """Run administrative tasks."""
    #run_sql_file()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'C2V2.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def run_sql_file():
    db_user = 'root'
    db_password = 'Testing321$'
    db_host = '127.0.0.1'  # or your MySQL server address
    sql_file_path = './C2V2/db.sql'
    # Connect to MySQL without specifying a database
    connection = pymysql.connect(
        user=db_user,
        password=db_password,
        host=db_host
    )
    cursor = connection.cursor()

    try:
        # Read the SQL file
        with open(sql_file_path, 'r') as sql_file:
            sql = sql_file.read()

        # Split SQL commands by semicolon
        sql_commands = sql.split(';')

        for command in sql_commands:
            command = command.strip()
            if command:  # Avoid executing empty commands
                cursor.execute(command)
                print(f"Executed: {command[:50]}...")  # Log the executed command

        connection.commit()
        print("Database initialized successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error initializing database: {e}")

    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    main()
