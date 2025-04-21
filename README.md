# Endpoint Monitor

This application monitors the availability of HTTP endpoints and calculates their uptime percentage. It includes mock servers with configurable failure rates for testing purposes.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Go](https://golang.org/dl/) (version 1.24)

## Setup

1. Clone this repository
2. Start the mock servers using Docker Compose:
   ```bash
   docker-compose up -d
   ```
   This will start three mock servers with different failure rates:
   - Server on port 8080 with 20% failure rate
   - Server on port 8081 with 50% failure rate
   - Server on port 8082 with 80% failure rate

## Configuration

The application uses a YAML configuration file to specify which endpoints to monitor. Here's the schema for the configuration file:

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
- name: sample body up
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body
  method: POST
  headers:
    content-type: application/json
  body: '{"foo":"bar"}'

- name: sample index up
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/

- name: sample 20%
  url: http://localhost:8080
```

## Running the Application

To run the application, use the following command:

```bash
go run main.go <config_file>
```

For example, to use the sample configuration:

```bash
go run main.go sample.yaml
```

## Output

The application will continuously monitor the specified endpoints and display:
- Current status (UP/DOWN) for each endpoint
- Availability percentage for each endpoint

Example output:
```
sample 20% is UP
http://localhost:8080 has 85.000000% availability
sample 50% is DOWN
http://localhost:8081 has 45.000000% availability
```

## Cleanup

To stop the mock servers:

```bash
docker-compose down
```

## Notes

- The application considers an endpoint as "UP" if:
  - The response status code is between 200 and 299
  - The response time is less than 500ms
  - No errors occurred during the request
- The monitoring interval is continuous (no sleep between checks)
- The application uses a 5-second timeout for HTTP requests 