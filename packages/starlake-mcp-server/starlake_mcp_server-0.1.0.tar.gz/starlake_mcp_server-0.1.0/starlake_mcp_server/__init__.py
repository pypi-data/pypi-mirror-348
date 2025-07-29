"""
Main entry point for the starlake_mcp_server package when imported or run as script.

Chooses between Low-Level Server (dynamic tools from OpenAPI spec) and
FastMCP Server (static tools) based on OPENAPI_SIMPLE_MODE env var.
"""

import os
import sys
from dotenv import load_dotenv
from starlake_mcp_server.logging_setup import setup_logging
from starlake_mcp_server.server_lowlevel import client
from starlake_mcp_server.server_lowlevel import run_server
from starlake_mcp_server.settings import DEBUG, PROJECT_ID

# Load environment variables from .env if present
load_dotenv()


def main():
    """
    Main entry point for starlake_mcp_server.

    Selects and runs either:
    - Low-Level Server (default, dynamic tools from OpenAPI spec)
    - FastMCP Server (OPENAPI_SIMPLE_MODE=true, static tools)
    """
    logger = setup_logging(debug=DEBUG)

    logger.debug("Starting starlake_mcp_server package entry point.")

    logger.debug("OPENAPI_SIMPLE_MODE is disabled. Launching Low-Level Server.")
    client.auth()
    client.select_project(PROJECT_ID)

    selected_server = run_server

    try:
        selected_server()
    except Exception as e:
        logger.critical("Unhandled exception occurred while running the server.", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
