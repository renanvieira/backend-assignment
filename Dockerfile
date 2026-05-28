FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev 

FROM python:3.13-alpine
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src ./src
COPY data ./data

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "src/main.py"]
CMD ["--output", "./data/output.csv"]
