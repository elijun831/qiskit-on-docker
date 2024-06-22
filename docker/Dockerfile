FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --ignore-pipfile

RUN pipenv run pip install jupyterlab

COPY . .

EXPOSE 8888

CMD ["pipenv", "run", "jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
