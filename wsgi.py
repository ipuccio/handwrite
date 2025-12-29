"""WSGI entry point for production deployment."""
from webapp.app import app

if __name__ == "__main__":
    app.run()
