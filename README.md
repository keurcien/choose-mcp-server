# Choose MCP Server Setup

## Pre-requisites

1. Start by downloading the Claude Desktop Client: https://claude.ai/download

2. Install `uv`

```
brew install uv
```

or

```
pip install uv
```

## Install the MCP server

1. Clone the repository

```
git clone git@github.com:keurcien/choose-mcp-server.git
cd choose-mcp-server
```

2. Install the dependencies in a virtual environment

```
uv sync
```

3. Install the server

```
uv run fastmcp install main.py
```

## Check that the MCP server has been correctly installed

Now you should see the Choose MCP server in the list of installed MCP servers:

```
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Open Claude Desktop and start asking questions.
