# Monitor Application

The Monitor application is a Flask service that continuously checks the health of configured HTTP endpoints and records metrics to MongoDB.

## Features

- Continuous monitoring of configured endpoints
- Configurable endpoints via YAML file
- Records health metrics to MongoDB
- Supports various HTTP methods and custom headers
- Configurable request timeouts and retry policies

## Configuration

The application uses a YAML configuration file to specify endpoints to monitor. The file location is provided as a command-line argument.

### Configuration Schema

```yaml
- name: string          # Name of the endpoint (for display purposes)
  url: string           # URL to monitor
  method: string        # HTTP method (optional, defaults to GET)
  headers:              # HTTP headers (optional)
    header-name: value
  body: string          # Request body (optional, for POST/PUT requests)
```

### Example Configuration

```yaml
- name: sample endpoint
  method: GET
  headers:
    content-type: application/json
```

## Running the Application

### Using Docker Compose
The application is configured to run as part of the Docker Compose setup. The configuration file is mounted at `/app/config.yaml`. Look at the `docker-compose.yaml` file to reconfigure the mount.

### Running Manually
```bash
python main.py <config_file>
```

## Data Storage

The application stores health metrics in MongoDB in the `health_metrics` collection. Each metric includes:
- Domain
- Start and end timestamps of each ping
- Successful requests and total number of requests in a given window by url

## Environment Variables

- `MONGODB_URI`: MongoDB connection string (default: mongodb://localhost:27017)
- `MONGODB_DB`: Database name (default: mongodb)

## Notes

- An endpoint is considered "UP" if:
  - The response status code is between 200 and 299
  - The response time is less than 500ms
- The application runs continuously without sleep between checks
- Metrics are stored in MongoDB for historical analysis
