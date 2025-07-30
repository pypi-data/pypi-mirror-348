# ChartMogul's MCP Server

## Usage
1. Open the Claude Desktop configuration file located at:
   * On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   * On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following:

```json
{
  "mcpServers": {
    "mcp-chartmogul": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/local/chartmogul-mcp-server",
        "run",
        "main.py"
      ],
      "env": {
        "CHARTMOGUL_TOKEN": "<YOUR-CHARTMOGUL-TOKEN>"
      }
    }
  }
}
```

3. Run `which uv` to locate the command entry for `uv` and replace it with the absolute path to the `uv` executable. 

4. Restart Claude Desktop to apply the changes.

## Development

1. Run `cp example.env .env` in the root of the repository to create a `.env` file.

2. Update it with the following env variables.
```bash
CHARTMOGUL_TOKEN=<YOUR-CHARTMOGUL-TOKEN>
```
3. Install `uv` by following the instructions [here](https://docs.astral.sh/uv/).

4. Run `uv sync` to install the dependencies. 

5. Run `source .venv/bin/activate` to activate the created virtual environment.

6. Run `mcp dev main.py` to start the MCP server.
