# application/view/app.py

import sys
import os
from flask import Flask
import logging

# Add the 'application' directory to the system path before importing other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard import create_dashboard  # Import Dash app
from routes import main_routes  # Import the blueprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize the Flask app
app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.urandom(24)  # For production, use a fixed secret key from environment variables

# Register the blueprint with the Flask app
app.register_blueprint(main_routes)

# Initialize the Dash app
create_dashboard(app)

# Debugging Route to List All Available Routes
@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {rule}")
        output.append(line)
    return '<br>'.join(output)

if __name__ == '__main__':
    logger.info("Starting the Flask application...")
    app.run(debug=True)
