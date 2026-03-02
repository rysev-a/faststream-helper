FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /usr/src/app
COPY ./services/api_gateway/* ./
COPY ./common ./common
RUN uv sync
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
