FROM python:3.11-bookworm

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.3

# Install required packages and Poetry
RUN apt-get update && apt-get install -y curl openssl && \
    curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Create a non-root user and necessary directories
RUN useradd -ms /bin/bash appuser && \
    mkdir -p /home/appuser/.jupyter /home/appuser/ssl_cert

# Generate SSL certificate
RUN openssl genrsa -out /home/appuser/ssl_cert/localhost.key 2048 && \
    openssl req -new -key /home/appuser/ssl_cert/localhost.key -out /home/appuser/ssl_cert/localhost.csr -subj "/CN=localhost" && \
    openssl x509 -req -days 365 -in /home/appuser/ssl_cert/localhost.csr -signkey /home/appuser/ssl_cert/localhost.key -out /home/appuser/ssl_cert/localhost.pem

# Copy JupyterLab config file
COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

# Change ownership of directories
RUN chown -R appuser:appuser /home/appuser/.jupyter /home/appuser/ssl_cert

# Switch to non-root user
USER appuser

# Expose port for JupyterLab
EXPOSE 8888

# Command to run JupyterLab
CMD ["poetry", "run", "jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--certfile=/home/appuser/ssl_cert/localhost.pem", "--notebook-dir=/app/notebooks"]
