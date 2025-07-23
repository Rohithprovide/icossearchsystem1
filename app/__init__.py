# Import the Flask app from the new location
from app.icos_core.app_init import app

# Make app available at module level
__all__ = ['app']
