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

RUN apt-get update && apt-get install -y \
    curl \
    openssl \
    nano \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

RUN mkdir -p /home/appuser/.jupyter /home/appuser/ssl_cert /app/notebooks && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /home/appuser/ssl_cert/localhost.key \
    -out /home/appuser/ssl_cert/localhost.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=OrganizationalUnit/CN=localhost" && \
    chmod 644 /home/appuser/ssl_cert/localhost.key /home/appuser/ssl_cert/localhost.pem

COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py
RUN chown -R root:root /home/appuser/.jupyter /home/appuser/ssl_cert /app/notebooks
EXPOSE 8888
CMD ["poetry", "run", "jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--certfile=/home/appuser/ssl_cert/localhost.pem", "--keyfile=/home/appuser/ssl_cert/localhost.key", "--notebook-dir=/app/notebooks"]
