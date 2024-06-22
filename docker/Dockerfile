FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --ignore-pipfile

RUN pipenv run pip install jupyterlab jupyterhub

COPY . .

EXPOSE 8888 8000

CMD ["pipenv", "run", "jupyterhub"]
