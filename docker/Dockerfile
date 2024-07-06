FROM python:3.11-bookworm
RUN pip install --no-cache-dir poetry==1.8.3
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

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./

()

COPY jupyter_lab_config.py /home/appuser/.jupyter/jupyter_lab_config.py

USER appuser

EXPOSE 8888

# Run JupyterLab
CMD ["poetry", "run", "jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
