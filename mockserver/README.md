# MockServer Application

The MockServer application is a Flask service that simulates HTTP endpoints with configurable failure rates. It's designed to help test and validate the monitoring system.

## Features

- Simulates HTTP endpoints with configurable failure rates
- Records all HTTP requests to MongoDB
- Configurable time windows for failure patterns
- Simple REST API for status checks
- Environment variable based configuration

## Configuration

The server can be configured using environment variables:

- `FLAKY_WINDOW`: Window duration in seconds
- `FLAKY_UP_RATIO`: Percentage of successful requests in 60 
- `MONGODB_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `MONGODB_DB`: Database name (default: monitoring)

## API Endpoints

- `GET /`: Returns info about the latest request

## Data Storage

The application stores HTTP request metrics in MongoDB in the `http_metrics` collection. Each metric includes:
- Request timestamp
- Request method and path
- Response status code

## Running the Application

### Using Docker Compose
The application is configured to run as part of the Docker Compose setup with three instances:
    - Server on port 5000 with 26% failure rate
    - Server on port 5001 with 50% failure rate
    - Server on port 5003 with 78% failure rate

### Running Manually
```bash
python app.py
```

## Notes

- The failure rate is calculated for all records i.e. all-time
- Requests are randomly failed based on the configured percentage
- All requests are logged to MongoDB for analysis
- The server is designed to be lightweight and fast
- Useful for testing the monitoring system's accuracy
