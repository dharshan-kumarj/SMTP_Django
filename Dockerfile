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

# Set Python path
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=smtp_project.settings

# Create necessary directories if they don't exist
RUN mkdir -p /app/smtp_project

# Run migrations and start server
CMD python manage.py migrate && \
    gunicorn --chdir /app smtp_project.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 2 --threads 2