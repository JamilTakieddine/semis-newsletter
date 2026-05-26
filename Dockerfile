# Slim Python base — keeps the image small for faster Cloud Run cold starts
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (Docker layer caching — only re-runs on requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Cloud Run Jobs run the container to completion and exit
# Env vars (API keys, email creds) are injected at runtime via Cloud Run secrets
CMD ["python", "main.py"]