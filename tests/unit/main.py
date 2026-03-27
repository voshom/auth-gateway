import logging
from flask import Flask, request

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define routes
@app.route('/auth', methods=['POST'])
def auth():
    # Extract the authorization request
    auth_request = request.get_json()

    # Validate the request
    if not auth_request:
        return 'Unauthorized', 401

    # Simulate a database query
    user_data = {'username': 'john_doe', 'password': 'secret'}

    # Compare the provided credentials with the stored ones
    if auth_request['username'] == user_data['username'] and auth_request['password'] == user_data['password']:
        return {'token': 'a_token'}  # Return a simulated token
    else:
        return 'Unauthorized', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)