# The builder image, used to build the virtual environment
FROM python:3.11-bookworm as builder

# Copy custom hosts file to /etc/hosts
COPY hosts /etc/hosts

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Environment variables for poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install dependencies without dev dependencies and clear cache
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-bookworm as runtime

# Install nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean

# Create a non-root user and group
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Environment variables for virtual environment
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy the virtual environment from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Ensure poetry is installed in the virtual environment
RUN .venv/bin/pip install --no-cache-dir poetry==1.8.3

# Copy Jupyter configuration file
COPY jupyter_lab_config.py ./

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Change ownership of the application files
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the ports for Nginx and JupyterLab
EXPOSE 8888
EXPOSE 5678
EXPOSE 8080
EXPOSE 443
EXPOSE 80

# Run JupyterLab through Nginx
CMD service nginx start && poetry run jupyter lab --ip=0.0.0.0 --no-browser --allow-root
