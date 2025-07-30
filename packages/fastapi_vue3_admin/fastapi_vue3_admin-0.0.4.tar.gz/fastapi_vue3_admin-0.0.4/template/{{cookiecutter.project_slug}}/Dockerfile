FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.7.1
RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml poetry.lock* README.md /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["{{ cookiecutter.project_slug }}", "dev", "--host", "0.0.0.0", "--port", "8000"] 