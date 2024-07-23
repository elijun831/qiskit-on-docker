FROM python:3.12-bookworm

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
    jq \
    apt-transport-https \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && mv /root/.local/bin/poetry /usr/local/bin/poetry \
    && poetry --version

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev \
    && mkdir -p /home/appuser/.jupyter /etc/ssl /app/notebooks /app/.Trash-0 /ssl \
    && if [ ! -f /ssl/tls.crt ] || [ ! -f /ssl/tls.key ] || [ ! -f /ssl/tls.csr ] || [ ! -f /ssl/tls.pem ]; then \
           openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
           -keyout /etc/ssl/tls.key \
           -out /etc/ssl/tls.crt \
           -subj "/C=US/ST=MA/L=Boston/O=Organization/OU=OrganizationalUnit/CN=localhost" \
           && openssl req -new -key /etc/ssl/tls.key -out /etc/ssl/tls.csr -subj "/C=US/ST=MA/L=Boston/O=Organization/OU=OrganizationalUnit/CN=localhost" \
           && cat /etc/ssl/tls.crt /etc/ssl/tls.key > /etc/ssl/tls.pem \
           && cp /etc/ssl/tls.key /ssl/tls.key \
           && cp /etc/ssl/tls.crt /ssl/tls.crt \
           && cp /etc/ssl/tls.csr /ssl/tls.csr \
           && cp /etc/ssl/tls.pem /ssl/tls.pem; \
       else \
           cp /ssl/tls.key /etc/ssl/tls.key \
           && cp /ssl/tls.crt /etc/ssl/tls.crt \
           && cp /ssl/tls.csr /etc/ssl/tls.csr \
           && cp /ssl/tls.pem /etc/ssl/tls.pem; \
       fi \
    && chmod 644 /etc/ssl/tls.key /etc/ssl/tls.crt /etc/ssl/tls.csr /etc/ssl/tls.pem \
    && chmod 777 /app/.Trash-0

COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

RUN echo '#!/bin/bash\n\
jupyter lab password\n\
sed -i "s/^c.ServerApp.password = .*/c.ServerApp.password = '\''$(cat /home/appuser/.jupyter/jupyter_server_config.json | jq -r .ServerApp.password)'\''/g" /home/appuser/.jupyter/jupyter_lab_config.py\n\
' > /usr/local/bin/change_jupyter_password && chmod +x /usr/local/bin/change_jupyter_password

RUN chown -R root:root /home/appuser/.jupyter /etc/ssl /app/notebooks /app/.Trash-0 /ssl

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--certfile=/etc/ssl/tls.crt", "--keyfile=/etc/ssl/tls.key", "--notebook-dir=/app/notebooks"]
