"""Vercel serverless function entrypoint for Flask application."""
from webapp.app import app

# Vercel expects the Flask app to be available as 'app'
# This module serves as the entrypoint for Vercel deployment
