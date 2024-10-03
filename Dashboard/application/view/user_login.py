# application/view/user_login.py

import bcrypt
from controller.db_connection import connect_db  # Adjust the import path as necessary
import logging

logger = logging.getLogger(__name__)

# Insert user with phone number
def insert_user(username, email, phone, password, role_name):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Get the role ID for the given role
        cursor.execute("SELECT id FROM roles WHERE role_name = %s", (role_name,))
        result = cursor.fetchone()
        if result:
            role_id = result[0]
        else:
            raise ValueError(f"Role '{role_name}' does not exist.")

        # Insert the user with role_id and phone number
        cursor.execute('''
            INSERT INTO users (username, email, phone, password, role_id) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (username, email, phone, hashed_password.decode('utf-8'), role_id))
        
        conn.commit()
        logger.info(f"User {username} inserted successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert user {username}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# User login
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Fetch user by username
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]

            # Check if the entered password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                logger.info(f"User {username} logged in successfully.")
                return True
            else:
                logger.warning(f"Incorrect password attempt for user {username}.")
                return False
        else:
            logger.warning(f"Login attempt with non-existent username: {username}.")
            return False
    except Exception as e:
        logger.error(f"Error during login for user {username}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
