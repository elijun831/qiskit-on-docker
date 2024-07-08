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
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version \
    && pip install jupyterlab

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev \
    && mkdir -p /home/appuser/.jupyter /home/appuser/ssl_cert /app/notebooks \
    && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
       -keyout /home/appuser/ssl_cert/localhost.key \
       -out /home/appuser/ssl_cert/localhost.pem \
       -subj "/C=US/ST=MA/L=Boston/O=Organization/OU=OrganizationalUnit/CN=localhost" \
    && chmod 644 /home/appuser/ssl_cert/localhost.key /home/appuser/ssl_cert/localhost.pem

COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

RUN echo '#!/bin/bash\n\
jupyter lab password\n\
sed -i "s/^c.ServerApp.password = .*/c.ServerApp.password = '\''$(cat /home/appuser/.jupyter/jupyter_server_config.json | jq -r .ServerApp.password)'\''/g" /home/appuser/.jupyter/jupyter_lab_config.py\n\
' > /usr/local/bin/change_jupyter_password && chmod +x /usr/local/bin/change_jupyter_password

RUN chown -R root:root /home/appuser/.jupyter /home/appuser/ssl_cert /app/notebooks

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--certfile=/home/appuser/ssl_cert/localhost.pem", "--keyfile=/home/appuser/ssl_cert/localhost.key", "--notebook-dir=/app/notebooks"]
