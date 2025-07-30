# Watson Discovery MCP Server

A Model Context Protocol (MCP) server that enables secure interaction with Watson Discovery. This server allows AI assistants to list projects, list collections in projects, execute queries through natural language processing.

## Features

- List available projects
- List available collections in project
- Execute queries in NLP in a collection



## Configuration

Set the following environment variables:

```bash
WATSONX_DISCOVERY_APIKEY=
WATSONX_DISCOVERY_URL=
WATSONX_DISCOVERY_VERSION=2023-03-31
```

## Usage

### With Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
	"mcpServers": {
		"watsonx-discovery": {
			"command": "wsl.exe",
			"args": [
				"bash",
				"-c",
				"/home/morpheus/.local/bin/uv --directory /home/morpheus/workspace/mcp-discovery run main.py"
			]
		}
	}
}
```

### As a standalone server

```bash
# Install dependencies
uv install 

# Run the server
uv run main-py
```

## Development

```bash
# Clone the repository
git clone https://github.com/matlock08/watson_discovery_mcp.git
cd watson_discovery_mcp

# Create virtual environment
uv venv 
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
uv install

# Run 
uv run main-py
```

## Security Considerations

- Never commit environment variables or credentials
- Use a database user with minimal required permissions
- Consider implementing query whitelisting for production use
- Monitor and log all database operations

## Security Best Practices

## License

MIT License - see LICENSE file for details.



uv run main.py



