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

EXPOSE 5000

# Set environment variables with defaults
ENV FLAKY_WINDOW=60
ENV FLAKY_UP_RATIO=0.8
ENV PID=mockserver

CMD ["poetry", "run", "python", "app.py"]
