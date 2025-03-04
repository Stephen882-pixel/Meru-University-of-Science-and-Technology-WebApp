# Build stage
FROM python:3.11-slim-bookworm as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Runtime stage
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=project.settings.production \
    PATH="/home/django/.local/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH" \
    PYTHONOPTIMIZE=1

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1000 django && \
    useradd -u 1000 -g django -d /app -s /bin/false django && \
    chown django:django /app

# Copy Python dependencies from builder
COPY --from=builder --chown=django:django /root/.local /home/django/.local

# Copy application code
COPY --chown=django:django . .

# Security hardening
RUN find /app -type d -exec chmod 755 {} \; && \
    find /app -type f -exec chmod 644 {} \; && \
    chmod 755 /app/manage.py

# Ensure Django is installed in the runtime environment
RUN pip install --user django

USER django

# Collect static files and migrate database
RUN python manage.py collectstatic --noinput --clear && \
    python manage.py migrate --noinput

# Application ports
EXPOSE 8000
