# Mock Server

A Flask-based mock server that logs HTTP requests to MongoDB.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

 poetry env use python


2. Make sure MongoDB is running locally on the default port (27017)

3. Create a `.env` file with your configuration (optional, defaults are provided)

## Running the Server

```bash
python -m mockserver.app
```

The server will start on `http://localhost:5000`

## Running Tests

```bash
pytest
```

## API Endpoints

### GET /
Logs a GET request to MongoDB and returns a success response.

### POST /
Logs a POST request to MongoDB and returns a success response.

## MongoDB Structure

Requests are stored in the `requests` collection with the following structure:
- method: HTTP method (GET/POST)
- headers: Request headers
- timestamp: UTC timestamp of the request
- data: Request body data (for POST requests)
