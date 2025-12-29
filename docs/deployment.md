# Deploying the Handwrite Web Application

The Handwrite project includes a Flask web application that allows users to generate custom fonts through a web interface.

## Prerequisites

Before deploying the web application, ensure you have:

1. Python 3.7 or higher installed
2. [fontforge](https://fontforge.org/en-US/) installed on the server
3. [Potrace](http://potrace.sourceforge.net/) installed on the server

## Local Development

### Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/builtree/handwrite.git
   cd handwrite
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (optional):
   ```bash
   cp .env.example .env
   # Edit .env and set SECRET_KEY to a random string
   ```

4. Run the development server:
   ```bash
   python webapp/app.py
   ```

5. Access the application at `http://localhost:5000`

## Production Deployment

### Using Gunicorn (Recommended)

For production environments, use Gunicorn as the WSGI server:

```bash
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 4
```

### Environment Variables

Set the following environment variables for production:

- `SECRET_KEY`: A secure random string for Flask session management
- `FLASK_ENV`: Set to `production` for production deployments
- `MAX_CONTENT_LENGTH`: Maximum file upload size in bytes (default: 16MB)

### Heroku Deployment

The application includes a `Procfile` for easy deployment to Heroku:

1. Create a Heroku app:
   ```bash
   heroku create your-app-name
   ```

2. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_ENV=production
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### Docker Deployment

You can containerize the application using Docker. Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fontforge \
    potrace \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
```

Build and run with environment variables:
```bash
docker build -t handwrite-webapp .
docker run -p 5000:5000 -e SECRET_KEY=your-secret-key handwrite-webapp
```

**Important**: Always pass `SECRET_KEY` as a runtime environment variable. Never hardcode secrets in the Dockerfile.

## Platform-Specific Notes

### System Dependencies

The web application requires the following system packages:

- **fontforge**: For font generation
- **potrace**: For converting bitmap images to vector graphics

Install on Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install fontforge potrace
```

Install on macOS:
```bash
brew install fontforge potrace
```

### File Upload Considerations

- Default max upload size is 16MB
- Temporary files are created during font generation and automatically cleaned up
- Ensure the server has sufficient disk space for temporary files

## Security Considerations

1. **SECRET_KEY**: Always use a strong, random secret key in production
2. **File Uploads**: The application validates file types (PNG, JPG only) and sizes
3. **Input Sanitization**: Font names are sanitized to prevent injection attacks
4. **HTTPS**: Always use HTTPS in production to protect uploaded files and session cookies

## Monitoring and Logging

The application uses Python's logging module. Configure logging level in production:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Troubleshooting

### Common Issues

1. **Font generation fails**: Ensure fontforge and potrace are installed and accessible
2. **Upload errors**: Check file size limits and file permissions
3. **Memory issues**: Consider reducing the number of workers or increasing server memory

## Scaling

For high-traffic deployments:

1. Use a reverse proxy (nginx, Apache) in front of Gunicorn
2. Implement a task queue (Celery, RQ) for font generation
3. Use a CDN for static assets
4. Consider horizontal scaling with multiple application servers
