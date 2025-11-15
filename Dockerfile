FROM python:3.12-slim

WORKDIR /app

# Install uv (modern pip replacement)
RUN pip install --no-cache-dir uv

# Copy only dependency metadata first (better caching)
COPY pyproject.toml ./


# Install dependencies directly from pyproject.toml
RUN uv pip install --system --no-cache .

# Copy the rest of your code
COPY . .

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "app"]
