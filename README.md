# Django SMTP Server

A high-performance Django project that handles contact form submissions with asynchronous email processing. Optimized for deployment on Render's free tier with instant API responses.

## Features

✅ **Async Email Queue** - Instant API responses (~50-200ms)
✅ **Background Email Processing** - Emails sent in separate thread
✅ **Optimized for Render** - No worker timeouts
✅ **Health Check Endpoint** - Monitoring support
✅ **Docker Support** - Easy deployment
✅ **CORS Enabled** - Ready for frontend integration

## Setup Instructions (with Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/dharshan-kumarj/SMTP_Django.git
cd SMTP_Django
```

### 2. Create a `.env` File

Create a `.env` file in the root directory of your project and add the following environment variables. Replace the placeholder values with your actual credentials.

```
SECRET_KEY=your_secret_key_here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password_here
```

**Note:** If using Gmail, you must enable 2-factor authentication in your Gmail account and generate an app-specific password to use as `EMAIL_HOST_PASSWORD`. [Follow this guide](https://support.google.com/accounts/answer/185833) to generate an app password.

### 3. Run with Docker Compose

The project is containerized with Docker for easy setup and deployment.

```bash
docker-compose up
```

This will:
- Build the Docker image if it doesn't exist
- Start the Django application with Gunicorn
- Apply any pending migrations
- Make the service available at http://localhost:8000

You should see output similar to:
```
Attaching to web-1
web-1  | Operations to perform:
web-1  |   Apply all migrations: admin, auth, contenttypes, sessions
web-1  | Running migrations:
web-1  |   No migrations to apply.
web-1  | [2025-02-14 02:16:49 +0000] [8] [INFO] Starting gunicorn 21.2.0
web-1  | [2025-02-14 02:16:49 +0000] [8] [INFO] Listening at: http://0.0.0.0:8000 (8)
web-1  | [2025-02-14 02:16:49 +0000] [8] [INFO] Using worker: sync
web-1  | [2025-02-14 02:16:49 +0000] [9] [INFO] Booting worker with pid: 9
```

### Alternative: Manual Setup (without Docker)

If you prefer to run without Docker:

1. **Create a Virtual Environment and Install Dependencies**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run Migrations**
```bash
python manage.py migrate
```

3. **Run the Server**
```bash
python manage.py runserver
```

## API Endpoints

### Submit Contact Form

* **URL:** `http://localhost:8000/api/contact/submit/`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`
* **Body:**

```json
{
    "name": "Test User",
    "email": "test@example.com",
    "message": "This is a test message!"
}
```

#### Example Request

You can use `curl` to submit a contact form:

```bash
curl -X POST http://localhost:8000/api/contact/submit/ \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message!"
    }'
```

#### Response

```json
{
    "status": "success",
    "message": "Your message has been queued and will be sent shortly"
}
```

**Note:** The API responds instantly. Emails are processed in the background and typically delivered within 1-3 seconds.

### Health Check

* **URL:** `http://localhost:8000/health/`
* **Method:** `GET`

Response:
```json
{
    "status": "healthy",
    "service": "smtp-django"
}
```

## Performance

- **API Response Time:** ~50-200ms (instant)
- **Email Queue Time:** < 50ms
- **Email Delivery:** 1-3 seconds (background)

The application uses an asynchronous queue system to process emails in a background thread, ensuring fast API responses without blocking.

## Project Structure

```
SMTP_Django/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── render.yaml              # Render deployment config
├── DEPLOYMENT.md            # Detailed deployment guide
├── smtp_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py            # Health check endpoint
│   ├── wsgi.py
│   ├── asgi.py
├── contact/
│   ├── __init__.py
│   ├── apps.py
│   ├── views.py            # Contact form handler
│   ├── tasks.py            # Async email queue
│   ├── urls.py
├── .env
├── requirements.txt
```

## Docker Configuration

The project includes Docker configuration files:

- `Dockerfile`: Defines the container image with Python and required dependencies
- `docker-compose.yml`: Orchestrates the service deployment with the right environment variables and port mappings

## Requirements

The `requirements.txt` file should include:

```
Django>=4.2.0
djangorestframework>=3.14.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
```

## Configuration Details

### Email Settings

This project uses Django's built-in email functionality with SMTP. The following settings are configured in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

## Production Deployment

### Deploy to Render

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for a complete deployment guide with:
- Step-by-step Render setup
- Performance optimizations
- Troubleshooting guide
- Monitoring tips

Quick deploy:
1. Push code to GitHub
2. Connect to Render
3. Add environment variables
4. Deploy!

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Generate a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS` in settings
4. Consider upgrading to PostgreSQL for persistent storage
5. Set up proper monitoring and logging

## Architecture

The application uses a queue-based architecture for optimal performance:

```
User Request → Django View (instant response ~50ms)
                      ↓
               Email Queue
                      ↓
          Background Worker Thread
                      ↓
          SMTP Server → Email Delivered (1-3s)
```

## Troubleshooting

### Common Issues

- **Email not sending**: Check that your SMTP credentials are correct and that your email provider allows SMTP access
- **Permission denied**: Ensure your app password is correct and that less secure apps are allowed (if applicable)
- **Connection errors**: Verify that your firewall allows outgoing connections on the SMTP port
- **Docker issues**: Make sure Docker and Docker Compose are installed correctly and running
- **Port conflicts**: Ensure that port 8000 is not being used by another service on your host

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

