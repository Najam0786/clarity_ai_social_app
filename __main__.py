# __main__.py
"""Main entry point to run the Social App via CLI."""

from .main import SocialApp  # 👈 relative import

if __name__ == "__main__":
    app = SocialApp()
    app.run()
