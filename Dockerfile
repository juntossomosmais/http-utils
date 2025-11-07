FROM python:3.13-slim

RUN apt update && apt install -y git && apt clean

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

# Poetry use this env var to authenticate
# https://python-poetry.org/docs/1.4/repositories/#configuring-credentials
ARG POETRY_HTTP_BASIC_AZURE_DEVOPS_PASSWORD

RUN poetry install --no-root

COPY . ./