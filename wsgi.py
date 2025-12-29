"""WSGI entry point for production deployment."""
from webapp.app import app

# Application is ready to be served by WSGI server
# Usage: gunicorn wsgi:app
