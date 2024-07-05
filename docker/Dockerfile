FROM python:3.11-bookworm

# Create a non-root user and group
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home --no-log-init appuser

# Set environment variables
ENV LANG C.UTF-8 \
    LC_ALL C.UTF-8 \
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

# Install curl and Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install JupyterLab globally
RUN pip install jupyterlab notebook voila

# Copy pre-configured Jupyter Notebook config
COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

# Install nginx, mkcert, and gettext-base for envsubst
RUN apt-get install -y libnss3-tools nginx gettext-base && apt-get clean && \
    curl -L https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64 -o /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert

# Create the certificates directory if it doesn't exist
RUN mkdir -p /etc/nginx/certs

# Install local CA for mkcert
RUN mkcert -install

# Generate the wildcard certificate using mkcert
RUN mkcert -cert-file /etc/nginx/certs/_wildcard.qiskitondocker.dev+3.pem -key-file /etc/nginx/certs/_wildcard.qiskitondocker.dev+3-key.pem "*.qiskitondocker.dev" localhost 127.0.0.1 ::1

# Generate the DH parameters file if it doesn't exist
RUN openssl dhparam -out /etc/nginx/certs/dhparam.pem 2048

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Set permissions for Nginx configuration and logs
USER root
RUN chown -R root:root /etc/nginx && \
    chown -R root:root /var/log/nginx && \
    chmod -R 755 /var/log/nginx

# Remove default Nginx configuration
RUN rm /etc/nginx/sites-enabled/default

# Copy Nginx configuration file template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Replace environment variables in the nginx.conf template and move to the correct location
RUN envsubst '\$STATIC_DIR' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Create a directory for notebooks
USER root
RUN mkdir -p /notebooks

# Specify the directory as a volume
VOLUME /notebooks

# Change ownership of the application files
USER root
RUN chown -R appuser:appuser /app

# Expose the ports for Nginx and JupyterLab
EXPOSE 8888 5678 8443 443 80

# Start Nginx and JupyterLab
CMD /bin/bash -c "envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;' & \
    jupyter lab --ip=0.0.0.0 --no-browser --allow-root --notebook-dir=/notebooks"
