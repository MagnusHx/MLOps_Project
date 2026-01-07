FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

# System dependencies
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency metadata
COPY pyproject.toml uv.lock README.md ./

# Install third-party dependencies (cached)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy application code
COPY src/ src/

# Install project itself
RUN uv sync --frozen

# Run evaluation
ENTRYPOINT ["uv", "run", "src/mlops_project/evaluate.py"]
