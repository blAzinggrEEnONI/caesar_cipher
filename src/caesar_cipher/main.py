"""
Main entry point for Caesar cipher CLI application.

This module is kept minimal - it only composes dependencies and runs the app.
All business logic is in the domain layer, all I/O is in adapters.
"""

from caesar_cipher.composition.container import compose_application

# Compose application with all dependencies wired
app = compose_application()


if __name__ == "__main__":
    app()
