"""
- OPENAPI_SPEC_URL: URL to the OpenAPI specification.
- TOOL_WHITELIST: Comma-separated list of allowed endpoint paths.
- SERVER_URL_OVERRIDE: Optional override for the base URL from the OpenAPI spec.
- API_KEY: Generic token for Bearer header.
- STRIP_PARAM: Param name (e.g., "auth") to remove from parameters.
- EXTRA_HEADERS: Additional headers in 'Header: Value' format, one per line.
- CAPABILITIES_TOOLS: Set to "true" to enable tools advertising (default: false).
- CAPABILITIES_RESOURCES: Set to "true" to enable resources advertising (default: false).
- CAPABILITIES_PROMPTS: Set to "true" to enable prompts advertising (default: false).
- ENABLE_TOOLS: Set to "false" to disable tools functionality (default: true).
- ENABLE_RESOURCES: Set to "true" to enable resources functionality (default: false).
- ENABLE_PROMPTS: Set to "true" to enable prompts functionality (default: false).
"""
import os
DEBUG = True # os.getenv("DEBUG", "").lower() in ("true", "1", "yes")
CAPABILITIES_TOOLS = os.getenv("CAPABILITIES_TOOLS", "true").lower() == "true"
CAPABILITIES_RESOURCES = os.getenv("CAPABILITIES_RESOURCES", "true").lower() == "true"
CAPABILITIES_PROMPTS = os.getenv("CAPABILITIES_PROMPTS", "true").lower() == "true"

SERVER_URL_OVERRIDE = os.getenv("SERVER_URL_OVERRIDE", "http://localhost:9000")
PROJECT_ID = os.getenv("PROJECT_ID", "101")

# Check feature enablement envvars (tools on, others off by default)
ENABLE_TOOLS = os.getenv("ENABLE_TOOLS", "true").lower() == "true"
ENABLE_RESOURCES = os.getenv("ENABLE_RESOURCES", "false").lower() == "true"
ENABLE_PROMPTS = os.getenv("ENABLE_PROMPTS", "false").lower() == "true"
OPENAPI_SPEC_URL = os.getenv("OPENAPI_SPEC_URL")
OPENAPI_SPEC_FORMAT = os.getenv("OPENAPI_SPEC_FORMAT", "json").lower()

STRIP_PARAM=os.getenv('STRIP_PARAM')
IGNORE_SSL_TOOLS = os.getenv('IGNORE_SSL_TOOLS', 'false')
IGNORE_SSL_SPEC = os.getenv('IGNORE_SSL_SPEC', 'false')
EXTRA_HEADERS = os.getenv('EXTRA_HEADERS')
TOOL_WHITELIST = os.getenv('TOOL_WHITELIST')


API_KEY = os.getenv("API_KEY", "25a3c0a890e008d2532c9aabbf88772b45a895dd096488ec4b4deae858b410b1")
API_AUTH_TYPE = os.getenv("API_AUTH_TYPE", "Bearer")
API_AUTH_HEADER = os.getenv("API_AUTH_HEADER", "Authorization")
