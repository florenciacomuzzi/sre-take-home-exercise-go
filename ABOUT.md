## Assumptions
- The user has a working knowledge of Python and the command line.
- The user has Docker and Docker Compose installed.
- The user has a basic understanding of HTTP methods and status codes.
- The user has a basic understanding of YAML configuration files.
- The user has a basic understanding of how to run applications in Docker containers.
- It is valuable to compare stats between the health check monitor and the actual requests on the 
server-side.
- Persisting metrics is important for historical analysis
- Various applications can benefit from stored metrics.

## Potential Improvements
- **CICD**: Fix linting errors, disable tests when there are none present
- **Testing**: Add more tests
- **Uptime simulation**: Simulate downtime for endpoints using more complex logic.
- **Robust database management**: Add performance improvements when reading and writing metrics.