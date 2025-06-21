"""
Redis KeyVault - A Python library for encrypted key-value storage using Redis Sentinel

This package provides secure storage and retrieval of sensitive information
using Redis Sentinel with Fernet encryption.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

from .redis_keyvault import (
    save_info,
    get_info,
    get_redis_connection,
    initialize_redis,
    create_new_env
)

__all__ = [
    "save_info",
    "get_info", 
    "get_redis_connection",
    "initialize_redis",
    "create_new_env"
]
