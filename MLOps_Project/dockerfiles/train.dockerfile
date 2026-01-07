FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt

RUN uv sync --frozen --no-install-project \
    apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY src src/
COPY data/ data/

RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "src/mlops_project/train.py"]
