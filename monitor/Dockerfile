FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

COPY . ./

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-cache --no-interaction --only main --no-ansi

# Set environment variables with defaults
ENV MONGODB_URI=mongodb://mongodb:27017/
ENV MONGODB_DB_NAME=mongodb
ENV MONGODB_USER=user
ENV MONGODB_PASSWORD=pass

# The configuration file will be mounted at runtime
CMD ["python", "main.py"]