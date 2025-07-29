"""
NewsAPI - A Python package for fetching and processing news from various sources
"""

__version__ = "1.0.3"

# Import main modules first
from . import auth
from . import database
from . import models
from . import schemas
from . import exceptions
from . import config
from . import logging_config

# Import subpackages
from . import routers
from . import services
from . import middleware
from . import utils

# Import main app object
from .main import app, run_app

__all__ = [
    'app',
    'run_app',
    'auth',
    'database',
    'models',
    'schemas',
    'exceptions',
    'config',
    'logging_config',
    'routers',
    'services',
    'middleware',
    'utils',
    '__version__'
]
