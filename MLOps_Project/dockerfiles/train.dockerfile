FROM nvcr.io/nvidia/pytorch:22.07-py3

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV UV_SYSTEM_PYTHON=1
ENV PYTHONPATH=/app/src


# Install uv (any recent version is fine)
RUN pip install --no-cache-dir "uv>=0.4.0"

# Copy dependency metadata
COPY pyproject.toml uv.lock README.md ./

# Install third-party dependencies INTO SYSTEM PYTHON
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ src/

# Install project INTO SYSTEM PYTHON
RUN uv sync --frozen

# IMPORTANT: run system python, not uv run
ENTRYPOINT ["python", "src/mlops_project/train.py"]
