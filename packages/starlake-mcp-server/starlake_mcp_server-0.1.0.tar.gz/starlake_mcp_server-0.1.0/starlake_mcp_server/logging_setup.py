"""
Logging setup for starlake-mcp-server.
"""

import os
import sys
import logging

from starlake_mcp_server.settings import DEBUG

# Initialize logger directly at module level
logger = logging.getLogger("starlake_mcp_server")

def setup_logging(debug: bool = False) -> logging.Logger:
    """Set up logging with the specified debug level."""
    # Logger is now initialized at module level, just configure it
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.debug("Logging configured")
    return logger

# Configure logger based on DEBUG env var when module is imported
setup_logging(DEBUG)