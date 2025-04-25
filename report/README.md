# Report Application

The Report application is a Flask service that displays metrics and statistics about endpoint availability. It provides a web interface to visualize the data collected by the Monitor and MockServer applications.

## Features

- Web-based dashboard for monitoring metrics
- Real-time availability statistics
- Historical data visualization
- Comparison between health checks and actual requests
- Simple and intuitive user interface

## Web Interface

The application provides a web interface accessible at http://localhost:5002 (configurable in docker-compose.yml) that displays:

- Overall uptime percentages
- Historical health metrics
- HTTP request patterns
- Comparison between health checks and actual requests
- Time-based availability trends
- Up status

### Screenshots

#### Report Dashboard Overview
![Report Dashboard Overview](images/report1.png)

#### Detailed Metrics View
![Detailed Metrics View](images/report2.png)

#### Historical Data Analysis
![Historical Data Analysis](images/report3.png)

## Data Sources

The application reads data from two MongoDB collections:
- `health_metrics`: Health check results from the Monitor application
- `http_metrics`: HTTP request records from the MockServer applications

## Configuration

The application can be configured using environment variables:

- `MONGODB_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `MONGODB_DB`: Database name (default: mongodb)
- `PORT`: Web server port (default: 5002)

## Running the Application

### Using Docker Compose
The application is configured to run as part of the Docker Compose setup.

### Running Manually
```bash
python app.py
```

## Notes

- The application calculates uptime based on all historical data
- Metrics are displayed in real-time as they are collected
- The interface is designed to be simple and easy to understand
- Data is read directly from MongoDB collections
- Port mappings can be modified in the docker-compose.yml file
