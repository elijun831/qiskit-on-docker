# The builder image, used to build the virtual environment
FROM python:3.11-bookworm as builder

# Create a non-root user and group
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

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

# ---------- Poetry installation
# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install dependencies without dev dependencies and clear cache
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy pre-configured Jupyter Notebook config
COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-bookworm as runtime

# Create Nginx user and group
RUN groupadd -r nginx && useradd -r -g nginx nginx

# Install nginx, mkcert, and gettext-base for envsubst
RUN apt-get update && apt-get install -y libnss3-tools nginx gettext-base && apt-get clean && \
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

# Set permissions and ownership for certificates
RUN chown nginx:nginx /etc/nginx/certs/*.pem && \
    chmod 666 /etc/nginx/certs/*.pem

# Copy the virtual environment from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Set permissions on the start script
COPY start.sh /start.sh

# Set execute permissions for start.sh and ensure it runs as root
RUN chmod +x /start.sh && \
    chown root:root /start.sh

# Switch to non-root user for security reasons
USER appuser

# Ensure poetry is installed in the virtual environment
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy Jupyter configuration file
COPY jupyter_lab_config.py ./

# Remove default Nginx configuration
USER root
RUN rm /etc/nginx/sites-enabled/default

# Copy Nginx configuration file
USER root
COPY nginx.conf /etc/nginx/nginx.conf.template

# ---------- Setting up directories, expose the ports, and start the JupyterLab
# Set up work directory
WORKDIR /app

# Create a directory for notebooks
RUN mkdir -p /notebooks

# Specify the directory as a volume
VOLUME /notebooks

# Change ownership of the application files
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the ports for Nginx and JupyterLab
EXPOSE 8888
EXPOSE 5678
EXPOSE 8443
EXPOSE 443
EXPOSE 80

# Start JupyterLab
ENTRYPOINT ["/bin/bash", "/start.sh"]
