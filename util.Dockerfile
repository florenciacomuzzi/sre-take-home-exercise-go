# syntax=docker/dockerfile:1
FROM golang:1.21-alpine

# Create app directory
WORKDIR /app

# Copy go.mod and go.sum first (allows caching of deps)
COPY go.mod go.sum ./
RUN go mod download

# Now copy the actual source files (doesn't bust cache if deps didn't change)
COPY ./util ./util

# Build the app
WORKDIR /app/util
RUN go build -o /app/server .

# Expose the port and run the binary
EXPOSE 8080
CMD ["/app/server"]