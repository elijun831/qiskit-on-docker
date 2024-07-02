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

# ---------- Poetry installation
# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
RUN touch README.md

# Install dependencies without dev dependencies and clear cache
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy pre-configured Jupyter Notebook config
COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

# ---------- Nginx installation and setup
# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-bookworm as runtime

# Install nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean

# Create a non-root user and group
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copy the virtual environment from the builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Ensure poetry is installed in the virtual environment
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Copy Jupyter configuration file
COPY jupyter_lab_config.py ./

# Remove default Nginx configuration
RUN rm /etc/nginx/sites-enabled/default

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/jupyter.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

# ---------- OpenSSL Certificate setup
# Create a directory to store the certificates
RUN mkdir -p /etc/nginx/certs

# OpenSSL certificate & dhparam generation script
WORKDIR /etc/nginx/certs  # Set the working directory for the commands

# Create the certificates directory if it doesn't exist
RUN mkdir -p /etc/nginx/certs

# Copy the script into the image
COPY generate_certs.sh /etc/nginx/certs/generate_certs.sh

# Make the script executable
RUN chmod +x /etc/nginx/certs/generate_certs.sh

# Execute the script
RUN /etc/nginx/certs/generate_certs.sh

# Create Nginx user and group 
RUN groupadd -r nginx && useradd -r -g nginx nginx

# Setting permissions and ownership
RUN chown nginx:nginx /etc/nginx/certs/*.pem && \
    chmod 600 /etc/nginx/certs/*.pem

# ---------- Setting up directories, expose the ports, and start the JupyterLab
# Set up work directory
WORKDIR /app

# Create a directory for notebooks
RUN mkdir -p /notebooks

# Specify the directory as a volume
VOLUME /notebooks

# Create non-root user for security
RUN adduser -u 5678 --disabled-password --gecos "" appuser

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

# Start JupyterLab
ENTRYPOINT ["/bin/bash", "/start.sh"]
