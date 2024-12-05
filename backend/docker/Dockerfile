FROM python:3.12 AS prod

WORKDIR /app/src
COPY pyproject.toml poetry.lock /app/src/

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    mv /root/.local/bin/poetry /usr/local/bin/poetry

ENV PATH="/root/.local/bin:${PATH}"
RUN poetry install --no-root --only main

COPY . .

RUN mv .env.deploy .env



