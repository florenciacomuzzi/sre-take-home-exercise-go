# syntax=docker/dockerfile:1
FROM golang:1.24-alpine

# Create app directory
WORKDIR /app

# Copy go.mod and go.sum first (allows caching of deps)
COPY go.mod go.sum ./
RUN go mod download

# Now copy the actual source files (doesn't bust cache if deps didn't change)
COPY . ./util

# Build the app
WORKDIR /app/util
RUN go build -o /app/server .

# Remove the static EXPOSE as we'll use dynamic ports
# Use an entrypoint script to handle the dynamic port
COPY <<EOF /app/entrypoint.sh
#!/bin/sh
export PORT=\${PORT:-8080}
/app/server
EOF

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]