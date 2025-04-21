from flask import Flask
import os
import random
import time

app = Flask(__name__)

# Get the success rate from environment variable, default to 100%
SUCCESS_RATE = float(os.getenv('SUCCESS_RATE', '100'))

def should_succeed():
    """Determine if the request should succeed based on the configured success rate."""
    return random.random() * 100 < SUCCESS_RATE

@app.route('/', methods=['GET', 'POST'])
def index():
    if should_succeed():
        # Return a random success code (200-299)
        return '', random.randint(200, 299)
    else:
        # Return a random error code (400-599)
        error_codes = list(range(400, 500)) + list(range(500, 600))
        return '', random.choice(error_codes)

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    # ... your routes and setup here ...
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
