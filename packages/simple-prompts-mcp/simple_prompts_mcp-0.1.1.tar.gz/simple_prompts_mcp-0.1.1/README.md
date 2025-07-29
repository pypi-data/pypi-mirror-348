# simple-prompts-mcp

## Overview

[日本語はこちら](README_ja.md)

- A simple MCP server for utilizing prompts.
- Prompts are defined in advance using YAML files.

## Defining Prompt Files

Define each prompt in a separate YAML file.

### Schema Details

- `name`: string. Identifier for the prompt.
- `description`: string. Description of the prompt.
- `arguments`: array. Each element is an object with the following properties:
    - `name`: string. Argument name.
    - `description`: string. Description of the argument.
    - `required`: boolean. Whether the argument is required.
- `prompt`: string. The main body of the prompt.  
  The prompt body (`prompt`) is dynamically generated using Python's `str.format()` with named arguments.  
  As shown in the example, you can use placeholders like `{user_name}` which will be replaced with the provided argument values.

### Example

```yaml
name: example
description: This is a sample prompt.
arguments:
  - name: user_name
    description: Name of the user
    required: true
prompt: |
  Hello, {user_name}!
```

Please create each YAML file according to this schema.

## Registering the MCP Server

To register `simple-prompts-mcp` as an MCP server, add the following to your configuration file.

> **Note:**  
> Please use Python 3.11 or later with `uv`.

```json
{
    "mcpServers": {
        "simple-prompts-mcp": {
            "command": "uvx",
            "args": ["simple-prompts-mcp"]
        }
    }
}
```

### Configuration

| Environment Variable | Purpose                        | Default Value                  |
|---------------------|--------------------------------|-------------------------------|
| `PROMPTS_DIR`       | Directory to store prompt files | ~/.config/simple-prompts-mcp  |


```json
{
    "mcpServers": {
        "simple-prompts-mcp": {
            "command": "uvx",
            "args": ["simple-prompts-mcp"],
            "env": {
                "PROMPTS_DIR": "/full-path/to/prompts/dir"
            }
        }
    }
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
