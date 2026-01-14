# Start with slim Python 3.13 image for smaller size
FROM python:3.13

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory inside container
WORKDIR /app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install all dependencies (pandas, sqlalchemy, psycopg2)
RUN uv sync --locked

# Copy ingestion script
COPY ingest_data.py homework.py ./

ENTRYPOINT ["bash"]

#CMD ["uv", "run", "python", "ingest_data.py", "--pg-host", "pgdatabase"]
#CMD ["uv", "run", "python", "homework.py", "--pg-host", "pgdatabase"]

# Set entry point to run the ingestion script
#ENTRYPOINT ["python", "homework.py"]
#ENTRYPOINT ["python", "ingest_data.py", "homework.py"]