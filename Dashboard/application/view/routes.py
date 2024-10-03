# application/view/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from user_login import insert_user, login_user  # Ensure correct import path
import logging

# Initialize the blueprint
main_routes = Blueprint('main_routes', __name__)

# Set up logging
logger = logging.getLogger(__name__)

@main_routes.route('/')
def home():
    return render_template('base.html')  # Ensure base.html exists

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Extract form data
            username = request.form['username']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            role_name = request.form['role_name']

            # Insert the user into the database
            insert_user(username, email, phone, password, role_name)

            flash(f"User {username} registered successfully!", "success")
            return redirect(url_for('main_routes.login'))  # Redirect to login after registration
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            flash(f"Error registering user: {str(e)}", "danger")

    return render_template('register.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            # Extract form data
            username = request.form['username']
            password = request.form['password']

            # Authenticate the user
            if login_user(username, password):
                session['logged_in'] = True
                session['username'] = username
                flash("Login successful!", "success")
                return redirect('/dashboard/')  # Redirect to the Dash dashboard
            else:
                flash("Invalid username or password!", "danger")
                return redirect(url_for('main_routes.login'))
        except Exception as e:
            logger.error(f"Error during login: {e}")
            flash(f"Error during login: {str(e)}", "danger")

    return render_template('login.html')

@main_routes.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('main_routes.login'))
