# application/controller/db_connection.py

import mysql.connector
from mysql.connector import Error
from config.config import DB_CONFIG

def connect_db():
    """
    Establishes a connection to the MySQL database using credentials from DB_CONFIG.
    Returns the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise
