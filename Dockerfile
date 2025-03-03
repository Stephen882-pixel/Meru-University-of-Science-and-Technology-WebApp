# Build stage
FROM python:3.11-slim-bookworm as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Runtime stage
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=project.settings.production \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Copy application
COPY . .

# Security hardening
RUN addgroup --system django && \
    adduser --system --ingroup django django && \
    chown -R django:django /app
USER django

# Collect static files
RUN python manage.py collectstatic --noinput --clear

EXPOSE 8000
CMD ["python", "manage.py", "runserver"]docker 