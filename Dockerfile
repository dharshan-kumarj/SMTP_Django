FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set Python path and environment variables
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=smtp_project.settings
ENV PYTHONUNBUFFERED=1

# Create necessary directories if they don't exist
RUN mkdir -p /app/smtp_project

# Collect static files (if needed in future)
RUN python manage.py collectstatic --noinput --clear || true

# Run migrations and start server with optimized settings
CMD python manage.py migrate --noinput && \
    gunicorn --chdir /app smtp_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --access-logfile - \
    --error-logfile - \
    --log-level info