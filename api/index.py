"""Vercel serverless function entrypoint for Flask application."""
from webapp.app import app

# Vercel expects the WSGI application to be available as 'app'
# The imported Flask app object is the WSGI callable that Vercel will invoke
# No additional assignment is needed since 'app' is already the Flask application instance
