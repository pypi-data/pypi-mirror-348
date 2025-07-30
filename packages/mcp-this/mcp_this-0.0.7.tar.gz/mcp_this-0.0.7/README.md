# MCP-This

> MCP Server that exposes CLI commands as tools using YAML files.

`mcp-this` is an MCP server creates tools from YAML configuration files to define which commands should be exposed as MCP tools, along with their parameters and execution details. This allows Claude to execute CLI commands without requiring you to write any code.

# Default Config

## Default Tools

If using the default config (no --tools, no --tools_path parameters) then 

TODO:

## Dependencies

Dependencies for default config (`configs/default.yaml`)

Mac:

```
brew install tree
brew install lynx
```

- `tree`- used in `get-directory-tree`
- `lynx` - used in `web-scrape`
    - `lynx -dump https://example.com`

