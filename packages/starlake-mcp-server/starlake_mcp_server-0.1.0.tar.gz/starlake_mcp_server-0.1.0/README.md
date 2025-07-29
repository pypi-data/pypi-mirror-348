# starlake-mcp-server


**starlake-mcp-server** is a Python package that implements a Model Context Protocol (MCP) server, designed to dynamically expose Starlake REST APIs— tagged as "mcp". 

## Table of Contents

- [starlake-mcp-server](#starlake-mcp-server)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [License](#license)




## Overview

https://github.com/user-attachments/assets/ed7102bf-2dcc-4d50-9356-597a9558d0a5

## Installation

Install the package directly from PyPI using the following command:

```bash
uvx starlake-mcp-server
```

To incorporate **starlake-mcp-server** into your MCP ecosystem configure it within your `mcpServers` settings.

```json

{
    "mcpServers": {
      "starlake-mcp-server": {
          "type": "stdio",
          "command": "uvx",
          "args": [
              "starlake-mcp-server"
          ],
          "env" : {
              "DEBUG": "false",
              "OPENAPI_SPEC_URL": "http://localhost:9000/docs/docs.yaml",
              "OPENAPI_SPEC_FORMAT": "yaml",
              "PROJECT_ID": "100",
              "API_KEY": "key as defined in the SL_API_CLI_KEY env var on the Starlake server side",
              "SERVER_URL_OVERRIDE": "http://localhost:9000",
              "API_AUTH_HEADER": "apiKey",
              "API_AUTH_TYPE": "api-key",
              "IGNORE_SSL_SPEC": "false",
              "ENABLE_TOOLS": "true"
          }
      }
    }
}

```


When running from a local source directory use the followig configuration instead.

```json

{
    "mcpServers": {
      "starlake-mcp-server": {
          "type": "stdio",
          "command": "uv",
          "args": [
              "--directory",
              "/Users/hayssams/git/public/starlake-mcp-server",
              "run",
              "starlake-mcp-server"
          ],
          "env" : {
              "DEBUG": "false",
              "OPENAPI_SPEC_URL": "http://localhost:9000/docs/docs.yaml",
              "OPENAPI_SPEC_FORMAT": "yaml",
              "PROJECT_ID": "100",
              "API_KEY": "key as defined in the SL_API_CLI_KEY env var on the Starlake server side",
              "SERVER_URL_OVERRIDE": "http://localhost:9000",
              "API_AUTH_HEADER": "apiKey",
              "API_AUTH_TYPE": "api-key",
              "IGNORE_SSL_SPEC": "false",
              "ENABLE_TOOLS": "true"
          }
      }
    }
}
```

## Environment Variables

- `DEBUG`: (Optional) Enables verbose debug logging when set to "true", "1", or "yes".
- `OPENAPI_SPEC_URL`: (Required) The URL to the OpenAPI specification JSON file for your starlake install (located in /docs/docs.yaml file).
- `PROJECT_ID`: (Required) Id of your Starlake API project
- `API_KEY`: (Required) Authentication token for the API sent as `api-key <API_KEY>` in the  header.
- `API_AUTH_TYPE`: (Required) Should be set to apiKey.
- `SERVER_URL_OVERRIDE`: (Required) Overrides the base URL of your Starlake API instance
- `IGNORE_SSL_SPEC`: (Optional) Set to `true` to disable SSL certificate verification when fetching the OpenAPI spec.
- `IGNORE_SSL_TOOLS`: (Optional) Set to `true` to disable SSL certificate verification for API requests made by tools.
- `ENABLE_TOOLS`: (Optional) Should we enable the tools available in the MCP server. Set to true

## License
This project is a fork of the mcp-openapi-proxy available here https://github.com/matthewhand/mcp-openapi-proxy

[MIT License](LICENSE)
