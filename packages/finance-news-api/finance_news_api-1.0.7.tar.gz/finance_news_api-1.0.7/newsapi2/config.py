# config.py
import os
import logging
from dotenv import load_dotenv

# Try to load from .env file, but don't fail if not found
try:
    load_dotenv()
except Exception as e:
    logging.warning(f"Could not load .env file: {e}")

# Set default API key if not provided in environment
DEFAULT_API_KEY = "development_key"  # Only for local development

# Get API key from environment with fallback to default (for development only)
API_KEY = os.getenv("API_KEY", DEFAULT_API_KEY)

# Configuration dictionary that can be expanded in the future
CONFIG = {
    "API_KEY": API_KEY,
    "DEBUG": os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
}

def get_config(key, default=None):
    """Get configuration value safely with fallback"""
    return CONFIG.get(key, default)