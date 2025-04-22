# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy poetry files
COPY pyproject.toml poetry.lock ./
COPY README.md ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
#
## Copy application code
#COPY . .
#
## Expose port
#EXPOSE 5000
#
## Set environment variables with defaults
#ENV FLAKY_WINDOW=60
#ENV FLAKY_UP_RATIO=0.8
#ENV PID=mockserver
#
## Run the application
#CMD ["poetry", "run", "python", "app.py"]
