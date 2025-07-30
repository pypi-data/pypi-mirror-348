# Swapnil MCP Server

[![PyPI version](https://img.shields.io/pypi/v/mistfs-mcp-server.svg)](https://pypi.org/project/mistfs-mcp-server/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mistfs-mcp-server.svg)](https://pypi.org/project/mistfs-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that provides automated utilities for Microsoft Visual Studio Team Foundation Server (TFS) repository management.

## Features

- Access TFS (Team Foundation Server) repositories using authenticated PAT connections
- Retrieve detailed commit history with user filtering
- Get current weather information for any city worldwide through OpenWeatherMap API

## Installation

```bash
pip install mistfs-mcp-server
```

### Requirements

- Python 3.9 or higher
- `mcp` package version 1.2.0 or higher
- Access to Microsoft Visual Studio Team Foundation Server
- Valid TFS Personal Access Token (PAT) with appropriate permissions

## Usage

### Starting the Server

```bash
# Run as a command
mistfs-mcp-server

# Or import in your Python code
from mistfs_tools.server import mcp
mcp.run()
```

### Using with MCP Clients

This package implements the Model Context Protocol (MCP), allowing AI assistants and other MCP-compatible clients to interact with Team Foundation Server.

Example of how an MCP client might use this tool:

```python
from mcp.client import Client

client = Client()

# Get repositories in a project
repos = await client.Get_Project_Repositories(project_name="MyProject")
print(repos)  # List of repository names in MyProject

# Get commit history for a specific user
commits = await client.Get_Repository_Checkins(
    project_name="MyProject",
    repository_name="MyRepo",
    userupn="user@company.com"
)
print(commits)  # List of commits by the specified user
```

## API Reference

### Get_Project_Repositories

Retrieves repositories from a specified Microsoft Visual Studio Team Foundation Server project.

**Parameters:**
- `project_name` (string, required): Name of the Microsoft Visual Studio Team Foundation Server project

**Features:**
- Authenticates using Personal Access Token (PAT)
- Makes HTTPS requests to TFS API
- Supports enterprise proxy configurations
- Includes detailed error handling and logging

**Returns:**
- List of repository names in the specified project, or an error message if the operation fails

### Get_Repository_Checkins

Retrieves commit history from a specified repository in Microsoft Visual Studio Team Foundation Server.

**Parameters:**
- `project_name` (string, required): Name of the project in Microsoft Visual Studio Team Foundation Server
- `repository_name` (string, required): Name of the repository to check
- `userupn` (string, required): User UPN to filter commits by author

**Features:**
- Filters commits by specific user
- Returns detailed commit information including IDs, authors, dates, and messages
- Requires TFS_PAT environment variable for authentication
- Supports secure HTTPS connections
- Includes proxy support for enterprise environments
- Comprehensive error handling and logging

**Returns:**
- List of commit details or appropriate error message

---

## Available Tools

| Tool                    | Description                                      |
|------------------------|--------------------------------------------------|
| Get_Project_Repositories| Retrieve repositories from Microsoft Visual Studio Team Foundation Server using PAT authentication |
| Get_Repository_Checkins | Retrieve detailed commit history from TFS repositories with user filtering |

## Development

### Project Structure

```
mistfs-mcp-server/
├── src/
│   └── mistfs_tools/
│       ├── __init__.py
│       ├── __main__.py
│       └── server.py
├── LICENSE
├── README.md
└── pyproject.toml
```

### Building and Publishing

```bash
python -m build
python -m twine upload dist/*
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- Swapnil Dagade (swapnildagade@gmail.com)

## Links

- [GitHub Repository](https://github.com/swapnildagade/mistfs-mcp-server)
- [Bug Tracker](https://github.com/swapnildagade/mistfs-mcp-server/issues)
- [Documentation](https://github.com/swapnildagade/mistfs-mcp-server#readme)
