FROM python:3.11-slim-bookworm

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
    POETRY_VERSION=1.8.3 \
    PATH="/root/.local/bin:$PATH" \
    NODE_PATH=/usr/lib/node_modules

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    gnupg \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && npm install -g configurable-http-proxy \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

RUN mkdir -p /etc/jupyterhub /home/appuser/ssl_cert /app/notebooks \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
       -keyout /home/appuser/ssl_cert/localhost.key \
       -out /home/appuser/ssl_cert/localhost.pem \
       -subj "/C=US/ST=MA/L=Boston/O=Organization/OU=OrganizationalUnit/CN=localhost" \
    && chmod 644 /home/appuser/ssl_cert/localhost.key /home/appuser/ssl_cert/localhost.pem

COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

RUN chown -R root:root /etc/jupyterhub /home/appuser/ssl_cert /app/notebooks

EXPOSE 8000

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
