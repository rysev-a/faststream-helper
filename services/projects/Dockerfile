FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /usr/src/app
COPY ./services/projects/pyproject.toml ./
COPY ./services/projects/app ./app
COPY ./common ./common
RUN uv sync
CMD ["uv", "run", "faststream", "run", "app.main:app"]
